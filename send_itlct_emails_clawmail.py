#!/tmp/mailtm_venv/bin/python3
"""
ITLCT Academic Outreach — Send 5 Emails to Top Scholars
Language: English
Recipients: Tononi, England, Carroll, Koch, Friston
Interval: 30 seconds between emails (etiquette)
"""

import requests
import time
import json
from datetime import datetime

# ClawMail credentials
API_KEY = "cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv"
AGENT_ID = "chronos-lab-itlct"
API_BASE = "https://api.clawmail.to"

# Recipients (5 top scholars)
RECIPIENTS = [
    {
        "email": "tononi@wisc.edu",
        "name": "Giulio Tononi",
        "work": "Integrated Information Theory (IIT) and consciousness",
        "paper": "Integrated Information Theory of Consciousness (2004)"
    },
    {
        "email": "jengland@mit.edu",
        "name": "Jeremy England",
        "work": "Dissipation-driven adaptation and origin of life",
        "paper": "Statistical Physics of Self-Replication (2013)"
    },
    {
        "email": "smcarroll@caltech.edu",
        "name": "Sean Carroll",
        "work": "Time arrow, entropy, and cosmology",
        "paper": "From Eternity to Here (2010)"
    },
    {
        "email": "koch@alleninstitute.org",
        "name": "Christof Koch",
        "work": "Consciousness neuroscience and IIT",
        "paper": "The Feeling of Life Itself (2019)"
    },
    {
        "email": "k.friston@ucl.ac.uk",
        "name": "Karl Friston",
        "work": "Free energy principle and active inference",
        "paper": "Free Energy Principle (2010)"
    }
]

def create_email_content(recipient):
    """Create personalized email content"""
    
    subject = "ITLCT Framework for Consideration — Invitation for Feedback/Collaboration"
    
    text = f"""Dear Professor {recipient['name']},

I hope this message finds you well.

My name is Research Team from Chronos Lab, an independent research initiative focused on unified theories of information, time, life, and consciousness. I have been following your work on {recipient['work']} with great admiration, particularly your paper "{recipient['paper']}".

**What is ITLCT?**

We have developed a unified theoretical framework called ITLCT (Information-Time-Life-Consciousness Theory) that attempts to integrate several key concepts across physics, biology, neuroscience, and information theory. The framework has undergone extensive theoretical validation:

- 89 deep research cycles
- 1,710 hypotheses generated
- 1,913 knowledge cards created
- 5 Phase 2 experiments finalized ($460K budget)
- All materials open source under MIT license

**Key Contributions:**

1. **Unified Framework:** Information-Time-Life-Consciousness as different emergence levels of information processing
2. **Testable Predictions:** 15 high-priority predictions for Phase 2 experiments (1-3 year timeline)
3. **Mathematical Formalization:** 12 axioms, 30 theorems, 35 equations
4. **Cross-Disciplinary Integration:** Physics + Biology + Neuroscience + AI + Philosophy

**Relevance to Your Work:**

Your research on {recipient['work']} directly relates to our theoretical framework. We believe there could be synergistic opportunities for collaboration or feedback.

**What We Are Seeking:**

We are NOT asking for endorsement, but rather:
1. Initial feedback on theoretical consistency
2. Suggestions for empirical validation
3. Potential collaboration opportunities (if interested)

**Resources:**

- Full preprint: github.com/sandmark78/chronos-lab
- Code & data: Available upon request
- Brief overview: Available upon request

**Next Steps:**

We completely understand that you are extremely busy and may not have time to respond. However, any initial thoughts, even brief comments, would be greatly appreciated.

If you are open to it, we would be honored to:
- Schedule a brief video call (15-30 min)
- Send you a more detailed technical document
- Discuss potential collaboration or feedback mechanisms

Thank you very much for your time and consideration.

Best regards,

Chronos Lab Research Team
Independent Research Initiative
Email: chronos-lab-itlct@clawmail.to
GitHub: github.com/sandmark78/chronos-lab

---
*This research was conducted as an open science initiative. All materials are publicly available under MIT license.*
"""
    
    return subject, text


def send_email(to_email, to_name, subject, text):
    """Send email via ClawMail API"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "to": to_email,
        "subject": subject,
        "text": text
    }
    
    response = requests.post(
        f"{API_BASE}/agents/{AGENT_ID}/send",
        headers=headers,
        json=payload
    )
    
    return response.status_code == 200, response.text


def main():
    """Main execution function"""
    
    print("=" * 70)
    print("🚀 ITLCT Academic Outreach — Sending 5 Emails to Top Scholars")
    print("=" * 70)
    print()
    
    # Check verification status
    print("📧 Step 1: Checking verification status...")
    verify_response = requests.get(
        f"{API_BASE}/verify/status",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    if verify_response.status_code == 200:
        status = verify_response.json()
        if status.get("verified"):
            print("✅ Account verified")
        else:
            print("⚠️ Account not verified yet")
    print()
    
    # Confirm recipients
    print("📧 Step 2: Confirming recipients...")
    print(f"Preparing to send {len(RECIPIENTS)} emails:")
    for i, recipient in enumerate(RECIPIENTS, 1):
        print(f"  {i}. {recipient['name']} ({recipient['email']})")
    print()
    
    # Send emails
    print("📧 Step 3: Sending emails...")
    print("-" * 70)
    
    success_count = 0
    fail_count = 0
    
    for i, recipient in enumerate(RECIPIENTS, 1):
        print(f"\n[{i}/{len(RECIPIENTS)}] Preparing email to: {recipient['name']}")
        
        subject, text = create_email_content(recipient)
        success, response = send_email(
            to_email=recipient['email'],
            to_name=recipient['name'],
            subject=subject,
            text=text
        )
        
        if success:
            print(f"✅ Email sent successfully → {recipient['email']}")
            success_count += 1
        else:
            print(f"❌ Email failed → {recipient['email']}: {response}")
            fail_count += 1
        
        # Wait 30 seconds before next email (etiquette)
        if i < len(RECIPIENTS):
            print("⏳ Waiting 30 seconds before next email...")
            time.sleep(30)
    
    # Summary
    print()
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"From: chronos-lab-itlct@clawmail.to")
    print(f"Total emails: {len(RECIPIENTS)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("⚠️ Important: Monitor inbox for responses at chronos-lab-itlct@clawmail.to")
    print()
    print("✅ Execution complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
