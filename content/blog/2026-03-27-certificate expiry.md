Title: Certificate expiry
Date: 2026-03-27
Category: Bitbucket
Tags: certificate, ssl, openssl, blog
Slug: certificate-expiry

In world where everything is connected and exposed to internet, interacting with self-signed certificates can be unique experience. 

I'll not explain here how certificated does work but focus on task which is work with such (self-signed - but not limited to those).

# How to 'get' remote certificate?

## Display certificates
```bash
openssl s_client -connect example.com:443 -showcerts
```

`-showcerts` - return complete certificate chain

## Server certificate
```bash
echo | openssl s_client -connect example.com:443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > server.crt
```

server.crt will look like:
```text
-----BEGIN CERTIFICATE-----
[Server Certificate Only]
-----END CERTIFICATE-----
```

## Certificate chain
```bash
echo | openssl s_client -showcerts -servername example.com -connect example.com:443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > chain.crt   
```

`-showcerts` - return complete certificate chain
`-servername` - Enable [SNI](https://en.wikipedia.org/wiki/Server_Name_Indication)

chain.crt  will look like:
```text
-----BEGIN CERTIFICATE-----
[Server Certificate]
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
[Intermediate Certificate 1]
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
[Intermediate Certificate 2]
-----END CERTIFICATE-----
```


In all cases when remote certificate expire - server or chain need to be updated.

# Certificate expiry

Speaking on expiry use this to see then certificate will expire:
```bash
echo | openssl s_client -showcerts -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate
```

This can be used in automation which when given criteria appear (eg. expiry in next 90/60/30 day) will sent notification.

# Automation

What about automation when there is more certificates manually checking them can be tedious and error prone ...

First thing is to have certificates locally to script.
I assume all certificates used in your deployment are stored in shared space available to all.

## Bash

```bash
#!/bin/bash

# Directory containing certificates (change this to your directory)
CERT_DIR="/path/to/certificates"

# Check if directory exists
if [ ! -d "$CERT_DIR" ]; then
    echo "Error: Directory $CERT_DIR does not exist"
    exit 1
fi

echo "=== Certificate Expiry Checker ==="
echo "Scanning directory: $CERT_DIR"
echo ""

# Counter for processed files
count=0

# Loop through each file in the directory
for cert_file in "$CERT_DIR"/*; do

    # Skip if not a regular file
    [ -f "$cert_file" ] || continue

    # Check if file contains a certificate (has BEGIN CERTIFICATE)
    if grep -q "BEGIN CERTIFICATE" "$cert_file" 2>/dev/null; then
        echo "File: $(basename "$cert_file")"

        # Extract and display expiry date
        expiry_date=$(openssl x509 -enddate -noout -in "$cert_file" 2>/dev/null | cut -d= -f2-)

        if [ -n "$expiry_date" ]; then
            echo " Expires: $expiry_date"

            # Convert to epoch for comparison (macOS and Linux compatible)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                expiry_epoch=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$expiry_date" +%s 2>/dev/null)
            
             else
                # Linux
                expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null)
             fi
             
             current_epoch=$(date +%s)
             
             # Calculate days until expiry
             if [ -n "$expiry_epoch" ]; then
                 days_left=$(( ($expiry_epoch - $current_epoch) / 86400 ))
                
                 if [ $days_left -lt 0 ]; then
                     echo "EXPIRED $(( -days_left )) days ago"
                 elif [ $days_left -lt 30 ]; then
                     echo " Expires in $days_left days (soon!)"
                else
                     echo " Valid for $days_left days"
                fi
            fi
        else
             echo "Could not read certificate"
        fi
        echo ""
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo "No certificate files found in $CERT_DIR"
else
    echo "=== Summary: $count certificate(s) processed ==="
fi
```

Example output:
```text
=== Certificate Expiry Checker ===  
Scanning directory: certs  

File: example_chain.crt  
 Expires: Oct 19 23:59:59 2026 GMT  
 Valid for 224 days
 
File: example_server.crt  
 Expires: Oct 19 23:59:59 2026 GMT  
 Valid for 224 days

=== Summary: 2 certificate(s) processed ===
```

Already here we can think of using bash to get more logic, sorting, etc.

## Ansible

File structure:
```bash
certs/ # <- directory with certificates in scope
check_local_cert_expiry.yml # <- below playbook
```

`check_local_cert_expiry.yml`

```yaml 
---
- name: Check Local Certificate Expiry
  hosts: localhost
  connection: local
  gather_facts: no
  
  vars:
    certs_dir: "{{ playbook_dir }}/certs"
    # Thresholds in days
    expiry_thresholds: [90, 60, 30]
    
  tasks:
    - name: Initialize results dictionary
      ansible.builtin.set_fact:
        expiry_results: {}
        all_certs_by_threshold: {}

    - name: Find certificate files in certs directory
      ansible.builtin.find:
        paths: "{{ certs_dir }}"
        patterns: "*.pem,*.crt"
        file_type: file
      register: cert_files
      delegate_to: localhost
      run_once: true

    - name: Read certificate subject and expiry
      ansible.builtin.shell:
        cmd: |
          openssl x509 -in "{{ item.path }}" -noout -subject -enddate
      register: cert_details
      changed_when: false
      failed_when: false
      delegate_to: localhost
      run_once: true
      loop: "{{ cert_files.files }}"
      loop_control:
        label: "{{ item.path | basename }}"

    - name: Process certificate expiry dates
      ansible.builtin.set_fact:
        processed_certs: >-
          {{
            processed_certs | default([]) + 
            [{
              'keystore': certs_dir,
              'keytool_path': 'openssl',
              'certs': [
                {
                  'alias': item.item.path | basename,
                  'subject': (item.stdout | regex_findall('^subject=(.+)$', multiline=True) | first | default('UNKNOWN')),
                  'expiry': (item.stdout | regex_findall('^notAfter=(.+)$', multiline=True) | first | default(''))
                }
              ]
            }]
          }}
      loop: "{{ cert_details.results }}"
      loop_control:
        label: "{{ item.item.path | basename }}"
      run_once: true

    - name: Check expiry status for each certificate
      ansible.builtin.shell:
        cmd: |
          EXPIRY_DATE="{{ item.1.expiry }}"
          CURRENT_DATE=$(date +%s)
          EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s 2>/dev/null || date -d "$(echo $EXPIRY_DATE | sed 's/\([A-Za-z]*\) \([0-9]*\) \([0-9:]*\) \([A-Z]*\) \([0-9]*\)/\5-\1-\2 \3/')" +%s 2>/dev/null)
          
          if [ $? -ne 0 ]; then
            echo "PARSE_ERROR"
            exit 0
          fi
          
          DAYS_REMAINING=$(( ($EXPIRY_EPOCH - $CURRENT_DATE) / 86400 ))
          
          if [ $DAYS_REMAINING -lt 0 ]; then
            echo "EXPIRED:$DAYS_REMAINING"
          elif [ $DAYS_REMAINING -le 30 ]; then
            echo "CRITICAL:$DAYS_REMAINING"
          elif [ $DAYS_REMAINING -le 60 ]; then
            echo "WARNING:$DAYS_REMAINING"
          elif [ $DAYS_REMAINING -le 90 ]; then
            echo "NOTICE:$DAYS_REMAINING"
          else
            echo "OK:$DAYS_REMAINING"
          fi
      register: expiry_status
      changed_when: false
      failed_when: false
      loop: "{{ processed_certs | subelements('certs') }}"
      loop_control:
        label: "{{ item.0.keystore }}: {{ item.1.alias }}"
      when: processed_certs is defined and processed_certs | length > 0

    - name: Build certificate expiry report
      ansible.builtin.set_fact:
        cert_expiry_report: >-
          {{
            cert_expiry_report | default([]) +
            [{
              'host': inventory_hostname,
              'keystore': item.item.0.keystore,
              'keytool_path': item.item.0.keytool_path,
              'alias': item.item.1.alias,
              'subject': item.item.1.subject,
              'expiry': item.item.1.expiry,
              'status': item.stdout.split(':')[0] if item.rc == 0 and ':' in item.stdout else 'UNKNOWN',
              'days_remaining': item.stdout.split(':')[1] | int if item.rc == 0 and ':' in item.stdout else 0
            }]
          }}
      loop: "{{ expiry_status.results }}"
      loop_control:
        label: "{{ item.item.0.keystore }}: {{ item.item.1.alias }}"
      when: expiry_status is defined and expiry_status.results is defined

    - name: Aggregate results from all hosts
      ansible.builtin.set_fact:
        all_expiry_results: "{{ ansible_play_hosts | map('extract', hostvars, 'cert_expiry_report') | select() | list | flatten }}"
      run_once: true

    - name: Categorize certificates by expiry status
      ansible.builtin.set_fact:
        expired_certs: "{{ all_expiry_results | selectattr('status', 'equalto', 'EXPIRED') | list }}"
        critical_certs: "{{ all_expiry_results | selectattr('status', 'equalto', 'CRITICAL') | list }}"
        warning_certs: "{{ all_expiry_results | selectattr('status', 'equalto', 'WARNING') | list }}"
        notice_certs: "{{ all_expiry_results | selectattr('status', 'equalto', 'NOTICE') | list }}"
      run_once: true

    - name: Display certificate expiry report header
      ansible.builtin.debug:
        msg:
          - ""
          - "================================================================"
          - "           CERTIFICATE EXPIRY STATUS REPORT"
          - "================================================================"
          - ""
          - "Report Date: {{ lookup('pipe', 'date +\"%%Y-%%m-%%d %%H:%%M:%%S\"') }}"
          - "Total Hosts: {{ ansible_play_hosts | length }}"
          - "Total Certificates Checked: {{ all_expiry_results | length }}"
          - ""
          - "================================================================"
      run_once: true

    - name: Display EXPIRED certificates
      ansible.builtin.debug:
        msg: |
          
          EXPIRED CERTIFICATES ({{ expired_certs | length }})
          ================================================================
          {% for cert in expired_certs %}
          Host: {{ cert.host }}
          Keystore: {{ cert.keystore }}
          Alias: {{ cert.alias }}
          Subject: {{ cert.subject }}
          Expiry Date: {{ cert.expiry }}
          Status: EXPIRED {{ cert.days_remaining }} days ago
          ----------------------------------------------------------------
          {% endfor %}
      run_once: true
      when: expired_certs | length > 0

    - name: Display CRITICAL certificates (≤30 days)
      ansible.builtin.debug:
        msg: |
          
          CRITICAL - Expiring in 30 days or less ({{ critical_certs | length }})
          ================================================================
          {% for cert in critical_certs | sort(attribute='days_remaining') %}
          Host: {{ cert.host }}
          Keystore: {{ cert.keystore }}
          Alias: {{ cert.alias }}
          Subject: {{ cert.subject }}
          Expiry Date: {{ cert.expiry }}
          Days Remaining: {{ cert.days_remaining }}
          ----------------------------------------------------------------
          {% endfor %}
      run_once: true
      when: critical_certs | length > 0

    - name: Display WARNING certificates (31-60 days)
      ansible.builtin.debug:
        msg: |
          
          WARNING - Expiring in 31-60 days ({{ warning_certs | length }})
          ================================================================
          {% for cert in warning_certs | sort(attribute='days_remaining') %}
          Host: {{ cert.host }}
          Keystore: {{ cert.keystore }}
          Alias: {{ cert.alias }}
          Subject: {{ cert.subject }}
          Expiry Date: {{ cert.expiry }}
          Days Remaining: {{ cert.days_remaining }}
          ----------------------------------------------------------------
          {% endfor %}
      run_once: true
      when: warning_certs | length > 0

    - name: Display NOTICE certificates (61-90 days)
      ansible.builtin.debug:
        msg: |
          
          NOTICE - Expiring in 61-90 days ({{ notice_certs | length }})
          ================================================================
          {% for cert in notice_certs | sort(attribute='days_remaining') %}
          Host: {{ cert.host }}
          Keystore: {{ cert.keystore }}
          Alias: {{ cert.alias }}
          Subject: {{ cert.subject }}
          Expiry Date: {{ cert.expiry }}
          Days Remaining: {{ cert.days_remaining }}
          ----------------------------------------------------------------
          {% endfor %}
      run_once: true
      when: notice_certs | length > 0

    - name: Display summary
      ansible.builtin.debug:
        msg: |
          
          ================================================================
                             SUMMARY
          ================================================================
          
          Expired:           {{ expired_certs | length }}
          Critical (≤30d):   {{ critical_certs | length }}
          Warning (31-60d):  {{ warning_certs | length }}
          Notice (61-90d):   {{ notice_certs | length }}
          OK (>90d):         {{ (all_expiry_results | selectattr('status', 'equalto', 'OK') | list | length) }}
          
          ================================================================
          
          {% if expired_certs | length > 0 or critical_certs | length > 0 %}
          ACTION REQUIRED: Certificates need immediate attention!
          {% elif warning_certs | length > 0 %}
          ATTENTION: Certificates will expire soon.
          {% elif notice_certs | length > 0 %}
          INFO: Some certificates will expire within 90 days.
          {% else %}
          All certificates are valid for more than 90 days.
          {% endif %}
          
          ================================================================

    - name: Fail if expired or critical certificates found
      ansible.builtin.fail:
        msg: "FAILURE: Found {{ expired_certs | length }} expired and {{ critical_certs | length }} critical certificates!"
      run_once: true
      when: 
        - (expired_certs | length > 0) or (critical_certs | length > 0)
        - fail_on_expiry | default(false) | bool
```

Example result:
```markdown

## EXPIRED CERTIFICATES (1)

**================================================================**

- **Host:** localhost
- **Keystore:** /path/to/certs
- **Alias:** expired_cert.crt
- **Subject:** C=US, ST=California, L=San Francisco, O=Dummy Certificates Inc., CN=expired.dummy.com
- **Expiry Date:** Feb 7 18:19:42 2026 GMT
- **Status: EXPIRED** (-30 days ago)

**----------------------------------------------------------------**

## WARNING - Expiring in 31-60 days (1)

**================================================================**

- **Host:** localhost
- **Keystore:** /path/to/certs
- **Alias:** expiring_32days_cert.crt
- **Subject:** C=US, ST=California, L=San Francisco, O=Dummy Certificates Inc., CN=expiring-32days.dummy.com
- **Expiry Date:** Apr 10 18:19:42 2026 GMT
- **Days Remaining: 31 days**

**----------------------------------------------------------------**
 
## OK (>90 days)

**================================================================**

- **Host:** localhost
- **Keystore:** /path/to/certs
- **Alias:** expiring_100days_cert.crt
- **Subject:** C=US, ST=California, L=San Francisco, O=Dummy Certificates Inc., CN=expiring-100days.dummy.com
- **Expiry Date:** Jun 18 18:19:42 2026 GMT
- **Days Remaining: 100 days**

**----------------------------------------------------------------**

## SUMMARY

**================================================================**

| Status               | Count |
|:--------------------:|:-----:|
| **Expired**          | 1     |
| **Critical (≤30d)**  | 0     |
| **Warning (31-60d)** | 1     |
| **Notice (61-90d)**  | 0     |
| **OK (>90d)**        | 1     |

**================================================================**

### **ACTION REQUIRED:**
- **1 certificate is EXPIRED** - Renew immediately!
- **1 certificate expires in 31 days** - Plan renewal soon
- **1 certificate is valid for 100 days** - No action needed

**================================================================**

```

