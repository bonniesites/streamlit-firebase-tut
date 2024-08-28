import streamlit as st
import subprocess
import os
import re
import pwd
from datetime import datetime, timedelta
import socket
import requests
import json
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import threading
import time
from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(filename='network_hardening.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

                    # Use environment variables for sensitive information
OTX_API_KEY = os.environ.get('OTX_API_KEY')
OTX_URL = os.environ.get('OTX_URL')

# Email configuration
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))

# Threat Intelligence API (example using OTX by AlienVault)
OTX_API_KEY = OTX_API_KEY
OTX_URL = "https://otx.alienvault.com/api/v1/indicators/submit_url/"

# Global variable to store changes for potential rollback
changes_made = []

def log_action(action):
    logging.info(action)
    changes_made.append(action)

def check_and_enable_firewall():
    st.write('Checking firewall status...')
    status = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
    st.write(f'Current firewall status is {status}')
    if 'Status: inactive' in status.stdout:
        st.write("Enabling firewall...")
        subprocess.run(['sudo', 'ufw', 'enable'], check=True)
    st.success("Firewall is active")
    log_action("Firewall enabled")

def configure_firewall_rules():
    st.write("Configuring firewall rules...")
    rules = [
        "sudo ufw default deny incoming",
        "sudo ufw default allow outgoing",
        "sudo ufw allow ssh",
        "sudo ufw allow http",
        "sudo ufw allow https"
    ]
    for rule in rules:
        subprocess.run(rule.split(), check=True)
        log_action(f"Firewall rule added: {rule}")
    st.success("Basic firewall rules configured")

def configure_ssh():
    config_file = '/etc/ssh/sshd_config'
    with open(config_file, 'r') as f:
        config = f.read()
    changes = {
        'PermitRootLogin': 'no',
        'PasswordAuthentication': 'no',
        'X11Forwarding': 'no',
        'MaxAuthTries': '3',
        'Protocol': '2'
    }
    for key, value in changes.items():
        pattern = rf'^{key}\s+.*$'
        replacement = f'{key} {value}'
        config = re.sub(pattern, replacement, config, flags=re.MULTILINE)
        if not re.search(pattern, config, re.MULTILINE):
            config += f'\n{replacement}'
    with open(config_file, 'w') as f:
        f.write(config)
    st.success("SSH configuration updated")
    log_action("SSH configuration updated")
    subprocess.run(['sudo', 'systemctl', 'restart', 'sshd'])

def thorough_ssh_check():
    st.write("Performing thorough SSH checks...")
    ssh_config = '/etc/ssh/sshd_config'
    with open(ssh_config, 'r') as f:
        config = f.read()    
    checks = {
        'PermitRootLogin': 'no',
        'PasswordAuthentication': 'no',
        'X11Forwarding': 'no',
        'MaxAuthTries': '3',
        'Protocol': '2',
        'PermitEmptyPasswords': 'no',
        'ClientAliveInterval': '300',
        'ClientAliveCountMax': '2'
    }    
    results = []
    for key, value in checks.items():
        if re.search(rf'^{key}\s+{value}', config, re.MULTILINE):
            results.append(f"[PASS] {key} is set to {value}")
        else:
            results.append(f"[FAIL] {key} is not set to {value}")    
    return results

def check_open_ports():
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    return result.stdout.splitlines()

def update_system():
    st.write("Updating system packages...")
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
    log_action("System packages updated")

def disable_unused_services():
    services_to_disable = ['telnet', 'rsh-server', 'xinetd']
    for service in services_to_disable:
        subprocess.run(['sudo', 'systemctl', 'stop', service], check=False)
        subprocess.run(['sudo', 'systemctl', 'disable', service], check=False)
        log_action(f"Service disabled: {service}")
    st.success("Unused services disabled")

def check_password_policy():
    st.write("Auditing password policies...")   
    with open('/etc/login.defs', 'r') as f:
        login_defs = f.read()
    policies = {
        'PASS_MAX_DAYS': '90',
        'PASS_MIN_DAYS': '10',
        'PASS_WARN_AGE': '7'
    }
    for policy, value in policies.items():
        pattern = rf'^{policy}\s+\d+$'
        replacement = f'{policy}\t{value}'
        login_defs = re.sub(pattern, replacement, login_defs, flags=re.MULTILINE)
        if not re.search(pattern, login_defs, re.MULTILINE):
            login_defs += f'\n{replacement}'
    with open('/etc/login.defs', 'w') as f:
        f.write(login_defs)
    st.success("Password policy updated")
    log_action("Password policy updated")

def audit_user_accounts():
    st.write("Auditing user accounts...")    
    def get_days_since_last_password_change(user):
        try:
            output = subprocess.run(['sudo', 'chage', '-l', user], capture_output=True, text=True, check=True)
            for line in output.stdout.splitlines():
                if "Last password change" in line:
                    date_str = line.split(':', 1)[1].strip()
                    last_change = datetime.strptime(date_str, "%b %d, %Y")
                    return (datetime.now() - last_change).days
        except subprocess.CalledProcessError:
            return None
        return None

    results = []
    for user in pwd.getpwall():
        if user.pw_uid >= 1000:  # Regular user accounts
            days_since_change = get_days_since_last_password_change(user.pw_name)
            if days_since_change is not None and days_since_change > 90:
                results.append(f"WARNING: Password for user {user.pw_name} hasn't been changed in {days_since_change} days")
    
    return results

def configure_automatic_updates():
    st.write("Configuring automatic updates...")   
    subprocess.run(['sudo', 'apt', 'install', 'unattended-upgrades', '-y'])
    subprocess.run(['sudo', 'dpkg-reconfigure', '-plow', 'unattended-upgrades'])
    st.success("Automatic updates configured")
    log_action("Automatic updates configured")

def check_common_vulnerabilities():
    st.write("Checking for common vulnerabilities...")    
    results = []    
    # Check for outdated packages
    outdated = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)
    if outdated.stdout.strip():
        results.append("WARNING: The following packages are outdated:")
        results.extend(outdated.stdout.splitlines())    
    # Check for open ports
    open_ports = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    results.append("Open ports (potential vulnerabilities):")
    results.extend(open_ports.stdout.splitlines())    
    # Basic check for default credentials
    default_users = ['admin', 'root', 'user', 'test']
    for user in default_users:
        try:
            pwd.getpwnam(user)
            results.append(f"WARNING: Default username '{user}' exists")
        except KeyError:
            pass    
    return results

def network_segmentation_check():
    st.write("Checking network segmentation...")
    results = []
    interfaces = os.listdir('/sys/class/net/')
    for interface in interfaces:
        if interface != 'lo':  # Exclude loopback
            addr = subprocess.run(['ip', '-4', 'addr', 'show', interface], capture_output=True, text=True)
            results.append(f"Interface {interface}:")
            results.extend(addr.stdout.splitlines())
    results.append("Review the network interfaces and ensure proper segmentation")
    return results

def setup_logging_and_alerting():
    st.write("Setting up basic logging and alerting...")
    subprocess.run(['sudo', 'apt', 'install', 'rsyslog', '-y'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'rsyslog'])
    subprocess.run(['sudo', 'systemctl', 'start', 'rsyslog'])    
    # Basic syslog configuration
    syslog_config = '''
    *.* @log_server:514  # Replace log_server with your actual log server
    '''
    with open('/etc/rsyslog.d/remote.conf', 'w') as f:
        f.write(syslog_config)    
    st.success("Basic logging configured. Remember to set up a log server and configure more detailed logging as needed.")
    log_action("Basic logging and alerting set up")

def generate_ansible_playbook():
    st.write("Generating Ansible playbook for configuration management...")
    playbook = {
        'name': 'Harden System',
        'hosts': 'all',
        'become': True,
        'tasks': [
            {'name': 'Update all packages', 'apt': {'upgrade': 'dist', 'update_cache': True}},
            {'name': 'Install required packages', 'apt': {'name': ['ufw', 'fail2ban', 'rkhunter'], 'state': 'present'}},
            {'name': 'Enable UFW', 'ufw': {'state': 'enabled'}},
            {'name': 'Allow SSH', 'ufw': {'rule': 'allow', 'port': '22'}},
            {'name': 'Enable fail2ban', 'systemd': {'name': 'fail2ban', 'state': 'started', 'enabled': True}},
            {'name': 'Run rkhunter', 'command': 'rkhunter --update --check'}
        ]
    }
    with open('harden_system.yml', 'w') as f:
        yaml.dump([playbook], f)
    st.success("Ansible playbook 'harden_system.yml' generated. Use 'ansible-playbook harden_system.yml' to run.")
    log_action("Ansible playbook generated")

def check_specific_vulnerabilities():
    st.write("Checking for specific vulnerabilities...")
    vulnerabilities = []
    # Check for CVE-2021-4034 (PwnKit)
    if os.path.exists('/usr/bin/pkexec') and os.stat('/usr/bin/pkexec').st_mode & 0o4000:
        vulnerabilities.append("System may be vulnerable to CVE-2021-4034 (PwnKit)")
    # Check for vulnerable Log4j versions (CVE-2021-44228)
    log4j_check = subprocess.run('find / -name "log4j-core*.jar"', shell=True, capture_output=True, text=True)
    if log4j_check.stdout:
        vulnerabilities.append("Potentially vulnerable Log4j versions found. Check for CVE-2021-44228")
    # Check for Shellshock vulnerability (CVE-2014-6271)
    shellshock_check = subprocess.run('env x="() { :;; }; echo vulnerable" bash -c "echo test"', shell=True, capture_output=True, text=True)
    if 'vulnerable' in shellshock_check.stdout:
        vulnerabilities.append("System may be vulnerable to Shellshock (CVE-2014-6271)")
    return vulnerabilities

def automated_response(vulnerabilities):
    st.write("Implementing automated responses to detected threats...")
    responses = []
    for vuln in vulnerabilities:
        if "PwnKit" in vuln:
            subprocess.run(['sudo', 'chmod', '0755', '/usr/bin/pkexec'])
            responses.append("Changed permissions on /usr/bin/pkexec to mitigate PwnKit vulnerability")
            log_action("Mitigated PwnKit vulnerability")
        elif "Log4j" in vuln:
            responses.append("Log4j vulnerability detected. Manual intervention required to update affected applications.")
        elif "Shellshock" in vuln:
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install', '--only-upgrade', 'bash'])
            responses.append("Attempted to update bash to address Shellshock vulnerability")
            log_action("Updated bash to address Shellshock vulnerability")
    return responses

def generate_report(all_results):
    st.write("Generating comprehensive report...")
    report = "Network Hardening Report\n"
    report += "========================\n\n"
    
    for section, results in all_results.items():
        report += f"{section}:\n"
        report += "-" * (len(section) + 1) + "\n"
        for item in results:
            report += f"- {item}\n"
        report += "\n"
    with open('hardening_report.txt', 'w') as f:
        f.write(report)
    st.success("Report generated: hardening_report.txt")
    # Email the report
    send_email_report(report)
    log_action("Comprehensive report generated and emailed")

def send_email_report(report):
    if not all([SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD]):
        st.error("Email configuration incomplete. Please set the SENDER_EMAIL, RECEIVER_EMAIL, and EMAIL_PASSWORD environment variables.")
        return

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = "Network Hardening Report"
    message.attach(MIMEText(report, "plain"))
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        st.success("Report emailed to admin")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")

def rollback_changes():
    st.warning("Rolling back changes...")
    for change in reversed(changes_made):
        # Implement specific rollback logic for each type of change
        if "firewall rule added" in change:
            # Remove the firewall rule
            rule = change.split(": ")[1]
            subprocess.run(f"sudo ufw delete {rule}", shell=True)
        elif "SSH configuration updated" in change:
            # Revert SSH configuration (this is a simplified example)
            subprocess.run("sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config", shell=True)
        elif "Service disabled" in change:
            # Re-enable the service
            service = change.split(": ")[1]
            subprocess.run(f"sudo systemctl enable {service}", shell=True)
            subprocess.run(f"sudo systemctl start {service}", shell=True)
        # Add more specific rollback actions as needed
        st.write(f"Rolled back: {change}")
    changes_made.clear()
    st.success("Rollback completed")
    log_action("Changes rolled back")

def check_threat_intelligence(ip_or_domain):
    if not OTX_API_KEY:
        st.error("OTX API key not set. Please set the OTX_API_KEY environment variable.")
        return []    
    headers = {'X-OTX-API-KEY': OTX_API_KEY}
    params = {'url': ip_or_domain}
    response = requests.get(OTX_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('pulse_info', {}).get('pulses', [])
    return []


def setup_mfa():
    st.write("Setting up Multi-Factor Authentication...")
    # This is a placeholder. In a real scenario, you'd integrate with your MFA solution
    subprocess.run(['sudo', 'apt', 'install', 'google-authenticator', '-y'])
    st.write("Google Authenticator installed. Please configure it for your users.")
    log_action("MFA setup initiated")

def monitor_changes():
    while True:
        # Monitor for unauthorized changes
        # This is a simplified example. In practice, you'd use tools like auditd or AIDE
        important_files = ['/etc/passwd', '/etc/shadow', '/etc/ssh/sshd_config']
        for file in important_files:
            if os.path.exists(file):
                current_mtime = os.path.getmtime(file)
                if 'last_mtime' not in monitor_changes.__dict__:
                    monitor_changes.last_mtime = {}
                if file not in monitor_changes.last_mtime:
                    monitor_changes.last_mtime[file] = current_mtime
                elif current_mtime != monitor_changes.last_mtime[file]:
                    logging.warning(f"File {file} has been modified!")
                    monitor_changes.last_mtime[file] = current_mtime
        time.sleep(60)  # Check every minute

# Start the monitoring thread
threading.Thread(target=monitor_changes, daemon=True).start()

def main():
    st.title("Advanced Network Hardening Tool")
    menu = st.sidebar.selectbox(
        "Choose a function",
        ["Firewall Configuration", "SSH Hardening", "Vulnerability Checks", "User Audit", 
         "Network Segmentation", "Logging Setup", "Ansible Playbook", "Threat Intelligence", 
         "Multi-Factor Authentication", "Generate Report", "Rollback Changes"]
    )

    if menu == "Firewall Configuration":
        st.header("Firewall Configuration")
        if st.button("Check and Enable Firewall"):
            check_and_enable_firewall()
        if st.button("Configure Firewall Rules"):
            configure_firewall_rules()

    elif menu == "SSH Hardening":
        st.header("SSH Hardening")
        if st.button("Configure SSH"):
            configure_ssh()
        if st.button("Thorough SSH Check"):
            results = thorough_ssh_check()
            for result in results:
                st.write(result)

    elif menu == "Vulnerability Checks":
        st.header("Vulnerability Checks")
        if st.button("Check Common Vulnerabilities"):
            results = check_common_vulnerabilities()
            for result in results:
                st.write(result)
        if st.button("Check Specific Vulnerabilities"):
            vulnerabilities = check_specific_vulnerabilities()
            for vuln in vulnerabilities:
                st.write(vuln)
            if st.button("Attempt Automated Response"):
                responses = automated_response(vulnerabilities)
                for response in responses:
                    st.write(response)

    elif menu == "User Audit":
        st.header("User Audit")
        if st.button("Audit User Accounts"):
            results = audit_user_accounts()
            for result in results:
                st.write(result)
        if st.button("Check Password Policy"):
            check_password_policy()

    elif menu == "Network Segmentation":
        st.header("Network Segmentation")
        if st.button("Check Network Segmentation"):
            results = network_segmentation_check()
            for result in results:
                st.write(result)

    elif menu == "Logging Setup":
        st.header("Logging Setup")
        if st.button("Setup Logging and Alerting"):
            setup_logging_and_alerting()

    elif menu == "Ansible Playbook":
        st.header("Ansible Playbook Generation")
        if st.button("Generate Ansible Playbook"):
            generate_ansible_playbook()

    elif menu == "Threat Intelligence":
        st.header("Threat Intelligence Check")
        ip_or_domain = st.text_input("Enter IP or Domain to check")
        if st.button("Check Threat Intelligence"):
            threats = check_threat_intelligence(ip_or_domain)
            if threats:
                st.warning(f"Potential threats found for {ip_or_domain}:")
                for threat in threats:
                    st.write(threat.get('name', 'Unknown threat'))
            else:
                st.success(f"No known threats found for {ip_or_domain}")

    elif menu == "Multi-Factor Authentication":
        st.header("Multi-Factor Authentication Setup")
        if st.button("Setup MFA"):
            setup_mfa()

    elif menu == "Generate Report":
        st.header("Generate Comprehensive Report")
        if st.button("Generate Report"):
            all_results = {
                'SSH Configuration': thorough_ssh_check(),
                'Open Ports': check_open_ports(),
                'User Accounts': audit_user_accounts(),
                'Common Vulnerabilities': check_common_vulnerabilities(),
                'Network Segmentation': network_segmentation_check(),
                'Specific Vulnerabilities': check_specific_vulnerabilities()
            }
            generate_report(all_results)

    elif menu == "Rollback Changes":
        st.header("Rollback Changes")
        if st.button("Rollback All Changes"):
            rollback_changes()

if __name__ == "__main__":
    main()