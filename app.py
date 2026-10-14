
import ipaddress
from urllib.parse import urlparse

import joblib
import pandas as pd
import streamlit as st

from src.feature_extraction import extract_features


st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🛡️",
    layout="wide",
)

# ---------- Load model ----------
@st.cache_resource
def load_model():
    return joblib.load("models/phishing_model.pkl")


model = load_model()


# ---------- Page design ----------
st.title("🛡️ Phishing Website Detector")
st.caption("Machine Learning • URL Security Analysis")

st.markdown(
    """
    Enter a website URL to check whether its URL characteristics
    resemble those associated with phishing websites.
    """
)

st.info(
    "🔒 Privacy: This application analyzes the URL text only. "
    "It does not open or visit the submitted website."
)

st.divider()


# ---------- URL input ----------
with st.form("url_analysis_form"):
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        help="Enter a complete URL, including http:// or https://",
    )

    analyze = st.form_submit_button(
        "🔍 Analyze Website",
        type="primary",
        use_container_width=True,
    )


# ---------- Analyze ----------
if analyze:
    cleaned_url = url.strip()

    if not cleaned_url:
        st.warning("Please enter a URL.")

    else:
        candidate = cleaned_url

        # Add a scheme only when the user omitted one.
        if "://" not in candidate:
            candidate = "https://" + candidate

        try:
            parsed = urlparse(candidate)
            hostname = parsed.hostname

            if (
                parsed.scheme not in ("http", "https")
                or not hostname
                or "." not in hostname and hostname != "localhost"
                or any(char.isspace() for char in candidate)
            ):
                st.error(
                    "Enter a valid website URL, such as "
                    "https://example.com"
                )

            else:
                # Validate a supplied port if present.
                try:
                    _ = parsed.port
                except ValueError:
                    st.error("The URL contains an invalid port.")
                    st.stop()

                # Keep the original text for analysis when a scheme
                # was already supplied.
                features = extract_features(candidate)
                feature_table = pd.DataFrame([features])

                prediction = int(model.predict(feature_table)[0])
                probabilities = model.predict_proba(feature_table)[0]

                # Use the model's actual class labels rather than
                # assuming the probability array's order.
                class_probabilities = dict(
                    zip(model.classes_, probabilities)
                )

                phishing_probability = float(
                    class_probabilities.get(0, 0.0)
                )
                legitimate_probability = float(
                    class_probabilities.get(1, 0.0)
                )

                st.divider()
                st.header("Analysis Result")
                st.code(candidate, language=None)

                left, right = st.columns([1, 1])

                with left:
                    if prediction == 0:
                        st.error(
                            "🚨 Potentially Phishing",
                            icon="🚨",
                        )
                        st.metric(
                            "Phishing model score",
                            f"{phishing_probability * 100:.2f}%",
                        )
                    else:
                        st.success(
                            "✅ Likely Legitimate",
                            icon="✅",
                        )
                        st.metric(
                            "Legitimate model score",
                            f"{legitimate_probability * 100:.2f}%",
                        )

                with right:
                    st.subheader("Model scores")
                    st.write("Phishing")
                    st.progress(phishing_probability)
                    st.write("Likely legitimate")
                    st.progress(legitimate_probability)

                st.caption(
                    "These scores are model estimates, not verified "
                    "probabilities that a site is safe or malicious."
                )

                st.divider()
                st.subheader("URL Characteristics")

                a, b, c, d = st.columns(4)

                a.metric("URL length", features["URLLength"])
                b.metric("Domain length", features["DomainLength"])
                c.metric("Digits", features["NoOfDegitsInURL"])
                d.metric("Subdomains", features["NoOfSubDomain"])

                e, f, g, h = st.columns(4)

                e.metric(
                    "HTTPS",
                    "Yes" if features["IsHTTPS"] else "No",
                )
                f.metric(
                    "IP address",
                    "Yes" if features["IsDomainIP"] else "No",
                )
                g.metric("Question marks", features["NoOfQMarkInURL"])
                h.metric("Ampersands", features["NoOfAmpersandInURL"])

                st.subheader("How to interpret the result")
                st.markdown(
                    """
                    - **Potentially Phishing:** Treat the URL cautiously.
                    - **Likely Legitimate:** The model did not identify
                      enough patterns to classify it as phishing.
                    - Neither result guarantees that a website is safe
                      or malicious. Do not enter passwords or payment
                      information based only on this result.
                    """
                )

        except Exception:
            st.error(
                "The URL could not be analyzed. Check the input and "
                "confirm that the saved model is available."
            )


# ---------- Footer ----------
st.divider()
st.caption(
    "Educational cybersecurity project • Random Forest classifier • "
    "URL-based analysis only"
)
