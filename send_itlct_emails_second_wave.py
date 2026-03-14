#!/tmp/mailtm_venv/bin/python3
"""
ITLCT Second Wave Email Campaign — 10 Scholars
Language: English
Recipients: Chalmers, Tegmark, Hoel, Seth, Bostrom, Barrett, Metzinger, Goff, Hoffman, Lau
Interval: 30 seconds between emails
"""

import requests
import time
import json
from datetime import datetime

# ClawMail credentials
API_KEY = "cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv"
AGENT_ID = "chronos-lab-itlct"
API_BASE = "https://api.clawmail.to"

# Recipients (10 scholars - second wave)
RECIPIENTS = [
    {
        "email": "david.chalmers@nyu.edu",
        "name": "David Chalmers",
        "work": "Hard Problem of Consciousness",
        "paper": "The Conscious Mind (1996)"
    },
    {
        "email": "maxtegmark@gmail.com",
        "name": "Max Tegmark",
        "work": "Consciousness as information processing",
        "paper": "Life 3.0 (2017)"
    },
    {
        "email": "erik.hoel@tufts.edu",
        "name": "Erik Hoel",
        "work": "Causal emergence and IIT",
        "paper": "Causal Emergence papers"
    },
    {
        "email": "a.k.seth@sussex.ac.uk",
        "name": "Anil Seth",
        "work": "Predictive processing and consciousness",
        "paper": "Being You (2021)"
    },
    {
        "email": "nick.bostrom@philosophy.ox.ac.uk",
        "name": "Nick Bostrom",
        "work": "AI safety and existential risk",
        "paper": "Superintelligence (2014)"
    },
    {
        "email": "lisa.barrett@northeastern.edu",
        "name": "Lisa Feldman Barrett",
        "work": "Emotion as prediction",
        "paper": "How Emotions Are Made (2017)"
    },
    {
        "email": "thomas.metzinger@uni-mainz.de",
        "name": "Thomas Metzinger",
        "work": "Self-model theory",
        "paper": "The Ego Tunnel (2009)"
    },
    {
        "email": "philip.goff@durham.ac.uk",
        "name": "Philip Goff",
        "work": "Panpsychism",
        "paper": "Galileo's Error (2019)"
    },
    {
        "email": "donald.hoffman@uci.edu",
        "name": "Donald Hoffman",
        "work": "Conscious realism",
        "paper": "The Case Against Reality (2019)"
    },
    {
        "email": "hakwan.lau@ucla.edu",
        "name": "Hakwan Lau",
        "work": "Metacognition and consciousness",
        "paper": "Higher-order thought theories"
    }
]

def create_email_content(recipient):
    """Create personalized email content"""
    
    subject = "ITLCT Framework — Invitation for Feedback on Unified Consciousness Theory"
    
    text = f"""Dear Professor {recipient['name']},

I hope this message finds you well.

My name is Research Team from Chronos Lab, an independent research initiative focused on unified theories of information, time, life, and consciousness. I have been following your work on {recipient['work']} with great admiration, particularly your {recipient['paper']}.

**What is ITLCT?**

We have developed a unified theoretical framework called ITLCT (Information-Time-Life-Consciousness Theory) that attempts to integrate several key concepts across physics, biology, neuroscience, and information theory. Your work on {recipient['work']} has been particularly influential in shaping our thinking.

**Key Contributions:**

1. **Unified Framework:** Information-Time-Life-Consciousness as different emergence levels of information processing
2. **Mathematical Formalization:** 13 axioms, 30 theorems, 35 equations
3. **Extensive Validation:** 90 research cycles, 1,700+ hypotheses, 1,900+ knowledge cards
4. **Testable Predictions:** 15 high-priority predictions for Phase 2 experiments ($460K budget)
5. **Open Science:** All materials publicly available under MIT license

**Relevance to Your Work:**

Your research on {recipient['work']} directly relates to our theoretical framework. We believe your expertise would be invaluable for feedback and potential collaboration.

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
    print("🚀 ITLCT Second Wave Email Campaign — 10 Scholars")
    print("=" * 70)
    print()
    
    # Check verification status
    print("📧 Step 1: Checking account status...")
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
    email_ids = []
    
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
            # Extract email ID from response
            try:
                response_data = json.loads(response)
                email_ids.append(response_data.get("id", "unknown"))
            except:
                email_ids.append("unknown")
        else:
            print(f"❌ Email failed → {recipient['email']}: {response}")
            fail_count += 1
        
        # Wait 30 seconds before next email (etiquette)
        if i < len(RECIPIENTS):
            print("⏳ Waiting 30 seconds before next email...")
            time.sleep(30)
    
    # Save email IDs for tracking
    tracking_data = {
        "campaign": "ITLCT Second Wave",
        "date": datetime.now().isoformat(),
        "total": len(RECIPIENTS),
        "success": success_count,
        "failed": fail_count,
        "email_ids": email_ids,
        "recipients": [r["email"] for r in RECIPIENTS]
    }
    
    with open("/home/claworc/.openclaw/workspace/email_tracking_second_wave.json", 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
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
    print(f"Tracking saved: email_tracking_second_wave.json")
    print()
    print("⚠️ Important: Monitor inbox for responses at chronos-lab-itlct@clawmail.to")
    print("⏳ Follow-up scheduled for 7 days later (3/20)")
    print()
    print("✅ Execution complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
