import "./LandingPage.css";

function LandingPage({ onGetStarted }) {
    return (
        <div className="landing-page">

            {/* ================= NAVBAR ================= */}
            <nav className="navbar">
                <div className="nav-container">

                    <div className="logo">
                        <div className="logo-icon">✚</div>

                        <div className="logo-text">
                            <span className="logo-main">MedExplain</span>
                            <span className="logo-ai">AI</span>
                        </div>
                    </div>

                    <div className="nav-links">
                        <a href="#features">Features</a>
                        <a href="#how-it-works">How it works</a>
                        <a href="#care">Why MedExplain</a>
                    </div>

                    <button
                        className="nav-button"
                        onClick={onGetStarted}
                    >
                        Try it now
                    </button>

                </div>
            </nav>


            {/* ================= HERO ================= */}
            <section className="hero-section">

                <div className="hero-container">

                    {/* LEFT SIDE */}
                    <div className="hero-content">

                        <div className="hero-badge">
                            <span className="badge-dot"></span>
                            AI-powered healthcare explanation
                        </div>

                        <h1>
                            Understand your
                            <span className="pink-text"> medical reports</span>
                            <br />
                            without the confusion.
                        </h1>

                        <p className="hero-description">
                            MedExplain AI transforms complex medical reports into
                            simple, easy-to-understand explanations so you can better
                            understand your health information.
                        </p>

                        <div className="hero-buttons">

                            <button
                                className="primary-button"
                                onClick={onGetStarted}
                            >
                                <span>📄</span>
                                Explore Report Reader
                            </button>

                            <button
                                className="secondary-button"
                                onClick={onGetStarted}
                            >
                                <span>💬</span>
                                Ask MedExplain AI
                            </button>

                        </div>

                        <div className="hero-trust">

                            <div className="trust-item">
                                <span className="trust-icon">✓</span>
                                Simple explanations
                            </div>

                            <div className="trust-item">
                                <span className="trust-icon">✓</span>
                                Report-based insights
                            </div>

                            <div className="trust-item">
                                <span className="trust-icon">✓</span>
                                Patient-friendly
                            </div>

                        </div>

                    </div>


                    {/* RIGHT SIDE */}
                    <div className="hero-visual">

                        <div className="floating-card card-one">
                            <div className="small-card-icon">✓</div>
                            <div>
                                <strong>Hemoglobin</strong>
                                <span>10.5 g/dL</span>
                            </div>
                        </div>

                        <div className="floating-card card-two">
                            <div className="small-card-icon pink-icon">♥</div>
                            <div>
                                <strong>Easy to understand</strong>
                                <span>AI explanation</span>
                            </div>
                        </div>


                        <div className="report-card">

                            <div className="report-header">

                                <div className="report-title-area">
                                    <div className="report-icon">✚</div>

                                    <div>
                                        <h3>Medical Report</h3>
                                        <p>Complete Blood Count</p>
                                    </div>
                                </div>

                                <span className="report-status">
                                    Analyzed
                                </span>

                            </div>


                            <div className="report-patient">
                                <div>
                                    <span>Patient</span>
                                    <strong>Sample Patient</strong>
                                </div>

                                <div>
                                    <span>Report Date</span>
                                    <strong>11 Sep 2026</strong>
                                </div>
                            </div>


                            <div className="report-divider"></div>


                            <div className="report-result">

                                <div className="result-heading">
                                    <span>Hemoglobin</span>
                                    <span className="result-low">LOW</span>
                                </div>

                                <div className="result-value">
                                    10.5
                                    <small>g/dL</small>
                                </div>

                                <div className="range-container">

                                    <div className="range-labels">
                                        <span>12.0</span>
                                        <span>16.0 g/dL</span>
                                    </div>

                                    <div className="range-bar">
                                        <div className="range-progress"></div>
                                    </div>

                                </div>

                            </div>


                            <div className="report-result normal-result">

                                <div className="result-heading">
                                    <span>WBC Count</span>
                                    <span className="result-normal">NORMAL</span>
                                </div>

                                <div className="result-value">
                                    8,500
                                    <small>/µL</small>
                                </div>

                                <div className="normal-range">
                                    Reference range: 4,000 – 11,000 /µL
                                </div>

                            </div>


                            <div className="ai-summary">

                                <div className="ai-summary-icon">
                                    ✨
                                </div>

                                <div>
                                    <strong>AI Summary</strong>

                                    <p>
                                        Your report contains mostly normal results.
                                        Hemoglobin is below the provided reference range.
                                    </p>
                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </section>


            {/* ================= INTRO ================= */}
            <section className="intro-section">

                <div className="section-container">

                    <div className="section-label">
                        WHY MEDEXPLAIN AI
                    </div>

                    <h2>
                        Medical reports shouldn't
                        <br />
                        feel like another language.
                    </h2>

                    <p className="section-description">
                        Lab reports contain numbers, abbreviations, reference ranges
                        and medical terminology that can be difficult to understand.
                        MedExplain AI helps turn that information into clear,
                        patient-friendly explanations.
                    </p>

                </div>

            </section>


            {/* ================= FEATURES ================= */}
            <section
                className="features-section"
                id="features"
            >

                <div className="section-container">

                    <div className="section-label">
                        FEATURES
                    </div>

                    <h2>
                        Everything you need to
                        <br />
                        understand your report.
                    </h2>


                    <div className="features-grid">

                        <div className="feature-card">

                            <div className="feature-icon">
                                📄
                            </div>

                            <h3>
                                Report Reader
                            </h3>

                            <p>
                                Upload a medical report and extract important
                                information automatically.
                            </p>

                            <button
                                className="feature-link"
                                onClick={onGetStarted}
                            >
                                Try Report Reader →
                            </button>

                        </div>


                        <div className="feature-card">

                            <div className="feature-icon">
                                🧠
                            </div>

                            <h3>
                                AI Explanation
                            </h3>

                            <p>
                                Understand medical terms and results through
                                simple, patient-friendly explanations.
                            </p>

                            <button
                                className="feature-link"
                                onClick={onGetStarted}
                            >
                                Explore AI →
                            </button>

                        </div>


                        <div className="feature-card">

                            <div className="feature-icon">
                                📊
                            </div>

                            <h3>
                                Result Analysis
                            </h3>

                            <p>
                                Quickly identify results that are low, normal,
                                or high according to the report's reference range.
                            </p>

                            <button
                                className="feature-link"
                                onClick={onGetStarted}
                            >
                                Analyze Results →
                            </button>

                        </div>


                        <div className="feature-card">

                            <div className="feature-icon">
                                💬
                            </div>

                            <h3>
                                Ask Questions
                            </h3>

                            <p>
                                Ask questions about your report and receive
                                easy-to-understand answers.
                            </p>

                            <button
                                className="feature-link"
                                onClick={onGetStarted}
                            >
                                Ask AI →
                            </button>

                        </div>

                    </div>

                </div>

            </section>


            {/* ================= HOW IT WORKS ================= */}
            <section
                className="how-section"
                id="how-it-works"
            >

                <div className="section-container">

                    <div className="section-label">
                        HOW IT WORKS
                    </div>

                    <h2>
                        From medical report
                        <br />
                        to simple explanation.
                    </h2>


                    <div className="steps-container">

                        <div className="step-card">

                            <div className="step-number">
                                01
                            </div>

                            <div className="step-icon">
                                📤
                            </div>

                            <h3>
                                Upload
                            </h3>

                            <p>
                                Upload your medical report as a PDF
                                or supported document.
                            </p>

                        </div>


                        <div className="step-line"></div>


                        <div className="step-card">

                            <div className="step-number">
                                02
                            </div>

                            <div className="step-icon">
                                🔍
                            </div>

                            <h3>
                                Analyze
                            </h3>

                            <p>
                                MedExplain extracts important values,
                                terms and reference ranges.
                            </p>

                        </div>


                        <div className="step-line"></div>


                        <div className="step-card">

                            <div className="step-number">
                                03
                            </div>

                            <div className="step-icon">
                                ✨
                            </div>

                            <h3>
                                Understand
                            </h3>

                            <p>
                                Receive a simple explanation and
                                an overall report summary.
                            </p>

                        </div>

                    </div>

                </div>

            </section>


            {/* ================= CARE SECTION ================= */}
            <section
                className="care-section"
                id="care"
            >

                <div className="care-container">

                    <div className="care-content">

                        <div className="section-label">
                            BUILT FOR CLARITY
                        </div>

                        <h2>
                            Healthcare information
                            <br />
                            should be easier to understand.
                        </h2>

                        <p>
                            MedExplain AI is designed to help patients make sense
                            of their reports without replacing professional medical
                            advice.
                        </p>


                        <div className="care-list">

                            <div className="care-item">
                                <div className="care-check">
                                    ✓
                                </div>

                                <div>
                                    <strong>
                                        Clear language
                                    </strong>

                                    <span>
                                        Complex medical terminology explained simply.
                                    </span>
                                </div>
                            </div>


                            <div className="care-item">
                                <div className="care-check">
                                    ✓
                                </div>

                                <div>
                                    <strong>
                                        Reference-aware
                                    </strong>

                                    <span>
                                        Results are compared with ranges provided in the report.
                                    </span>
                                </div>
                            </div>


                            <div className="care-item">
                                <div className="care-check">
                                    ✓
                                </div>

                                <div>
                                    <strong>
                                        Safety first
                                    </strong>

                                    <span>
                                        Designed to explain information, not provide a diagnosis.
                                    </span>
                                </div>
                            </div>

                        </div>

                    </div>


                    <div className="care-visual">

                        <div className="care-circle">

                            <div className="heart-symbol">
                                ♥
                            </div>

                            <span>
                                Understand
                            </span>

                            <strong>
                                Your Health
                            </strong>

                        </div>

                    </div>

                </div>

            </section>


            {/* ================= FINAL CTA ================= */}
            <section className="final-cta">

                <div className="cta-container">

                    <div className="cta-icon">
                        ✨
                    </div>

                    <h2>
                        Ready to understand
                        <br />
                        your medical report?
                    </h2>

                    <p>
                        Start exploring MedExplain AI and turn complex
                        medical information into something easier to understand.
                    </p>

                    <button
                        className="cta-button"
                        onClick={onGetStarted}
                    >
                        Get Started
                        <span>→</span>
                    </button>

                </div>

            </section>


            {/* ================= FOOTER ================= */}
            <footer className="footer">

                <div className="footer-container">

                    <div className="footer-brand">

                        <div className="logo">

                            <div className="logo-icon">
                                ✚
                            </div>

                            <div className="logo-text">
                                <span className="logo-main">
                                    MedExplain
                                </span>

                                <span className="logo-ai">
                                    AI
                                </span>
                            </div>

                        </div>

                        <p>
                            Making medical information easier
                            to understand.
                        </p>

                    </div>


                    <div className="footer-links">

                        <div>
                            <h4>
                                Product
                            </h4>

                            <a href="#features">
                                Features
                            </a>

                            <a href="#how-it-works">
                                How it works
                            </a>

                            <button onClick={onGetStarted}>
                                Try MedExplain
                            </button>
                        </div>


                        <div>
                            <h4>
                                Important
                            </h4>

                            <a href="#care">
                                Safety
                            </a>

                            <a href="#care">
                                Privacy
                            </a>

                            <a href="#care">
                                Disclaimer
                            </a>
                        </div>

                    </div>

                </div>


                <div className="footer-bottom">

                    <p>
                        © 2026 MedExplain AI. Built for educational purposes.
                    </p>

                    <p>
                        MedExplain AI does not replace professional medical advice.
                    </p>

                </div>

            </footer>

        </div>
    );
}

export default LandingPage;