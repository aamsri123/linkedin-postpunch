import anthropic
import streamlit as st

API_KEY = st.secrets["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=API_KEY)

def call_claude(system_prompt, content):
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": content}]
    )
    return message.content[0].text

def hook_agent(post):
    return call_claude(
        "You are a LinkedIn hook expert. Analyze only the FIRST LINE of this post. Rate it 1-10 and explain if it would stop someone from scrolling. Suggest a stronger opening if needed.",
        f"Analyze this LinkedIn post:\n\n{post}"
    )

def tone_agent(post):
    return call_claude(
        "You are a tone and authenticity expert. Does this post sound like a real human or corporate fluff? Is it humble, arrogant, inspiring, or generic? Give specific feedback.",
        f"Analyze this LinkedIn post:\n\n{post}"
    )

def engagement_agent(post):
    return call_claude(
        "You are a LinkedIn engagement expert. Will this post get comments, shares, and reactions? What's missing — a question, a story, a controversy, a call to action? Be specific.",
        f"Analyze this LinkedIn post:\n\n{post}"
    )

def hashtag_agent(post):
    return call_claude(
        "You are a LinkedIn hashtag strategist. Review the hashtags used. Are they relevant, too broad, too niche? Suggest 5 better hashtags with a reason for each.",
        f"Analyze this LinkedIn post:\n\n{post}"
    )

def report_agent(hook, tone, engagement, hashtags, original_post):
    return call_claude(
        """You are a LinkedIn content strategist. Based on the agent feedback, do two things:
1. Give an overall score out of 10 on the FIRST LINE in this exact format: SCORE: X/10
2. Write a full improved version of the post incorporating all feedback. Make it punchy and human.""",
        f"""Original post:
{original_post}

Hook review: {hook}
Tone review: {tone}
Engagement review: {engagement}
Hashtag review: {hashtags}"""
    )

# Page config must be first
st.set_page_config(page_title="LinkedIn PostPunch", page_icon="🧠", layout="wide")

# Sidebar
with st.sidebar:
    st.title("📖 How to use")
    st.write("1. Paste your LinkedIn post draft")
    st.write("2. Click **Review My Post**")
    st.write("3. Read feedback from 5 AI agents")
    st.write("4. Copy the improved version")
    st.markdown("---")
    st.caption("Built with Claude AI + Streamlit")

# Main UI
st.title("🧠 LinkedIn PostPunch")
st.write("5 AI agents review your LinkedIn draft and rewrite it for maximum impact.")

post_input = st.text_area("Paste your LinkedIn post draft here", height=200, placeholder="I'm excited to share...")

if st.button("🚀 Review My Post", type="primary"):
    if not post_input.strip():
        st.warning("Please paste a post first.")
    else:
        with st.spinner("Running 5 agents... this takes about 15 seconds"):
            hook = hook_agent(post_input)
            tone = tone_agent(post_input)
            engagement = engagement_agent(post_input)
            hashtags = hashtag_agent(post_input)
            report = report_agent(hook, tone, engagement, hashtags, post_input)

        # Extract and show score
        score_line = [l for l in report.split("\n") if "SCORE:" in l]
        if score_line:
            score = score_line[0].replace("SCORE:", "").strip()
            st.metric(label="Overall Score", value=score)

        st.markdown("---")

        with st.expander("🎯 Hook Agent", expanded=True):
            st.write(hook)

        with st.expander("💬 Tone Agent", expanded=True):
            st.write(tone)

        with st.expander("📈 Engagement Agent", expanded=True):
            st.write(engagement)

        with st.expander("#️⃣ Hashtag Agent", expanded=True):
            st.write(hashtags)

        with st.expander("📋 Final Rewrite", expanded=True):
            rewrite = "\n".join([l for l in report.split("\n") if "SCORE:" not in l]).strip()
            st.write("**Copy this improved version:**")
            st.code(rewrite, language=None)
