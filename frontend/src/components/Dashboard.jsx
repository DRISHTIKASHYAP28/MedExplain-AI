import { useState } from "react";
import "./Dashboard.css";
// =========================================================
// CLEAN AI CHAT TEXT
// =========================================================

const cleanAiText = (text) => {
    if (!text) {
        return "";
    }

    return String(text)
        // Remove escaped markdown
        .replace(/\\\*\\\*/g, "")
        .replace(/\\\*/g, "")
        .replace(/\\#/g, "#")

        // Remove bold markdown
        .replace(/\*\*(.*?)\*\*/g, "$1")

        // Remove italic markdown
        .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "$1")

        // Remove markdown headings
        .replace(/^#{1,6}\s*/gm, "")

        // Convert markdown bullets to normal bullets
        .replace(/^\s*[-*+]\s+/gm, "• ")

        // Remove markdown horizontal lines
        .replace(/^\s*---+\s*$/gm, "")

        .trim();
};


function Dashboard({ onBack }) {

    const [activeTab, setActiveTab] = useState("pdf");

    const [file, setFile] = useState(null);

    const [writtenReport, setWrittenReport] = useState("");

    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const [isChatting, setIsChatting] = useState(false);

    const [result, setResult] = useState(null);

    const [error, setError] = useState("");

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);


    // =========================================================
    // TAB CHANGE
    // =========================================================

    const handleTabChange = (tab) => {

        setActiveTab(tab);

        setFile(null);

        setWrittenReport("");

        setResult(null);

        setError("");

        setQuestion("");

        setMessages([]);
    };


    // =========================================================
    // FILE CHANGE
    // =========================================================

    const handleFileChange = (event) => {

        const selectedFile =
            event.target.files?.[0];

        if (!selectedFile) {
            return;
        }

        setFile(selectedFile);

        setResult(null);

        setError("");

        setMessages([]);
    };


    // =========================================================
    // ANALYZE REPORT
    // =========================================================

    const handleAnalyze = async () => {

        setError("");

        setResult(null);

        setMessages([]);

        if (activeTab !== "write" && !file) {

            setError(
                "Please choose a report first."
            );

            return;
        }

        if (
            activeTab === "write" &&
            !writtenReport.trim()
        ) {

            setError(
                "Please enter your medical report first."
            );

            return;
        }


        const formData = new FormData();


        if (activeTab === "write") {

            formData.append(
                "report_text",
                writtenReport
            );

        } else {

            formData.append(
                "file",
                file
            );
        }


        try {

            setIsAnalyzing(true);

            const response = await fetch(
                "https://backend-pink-five-90.vercel.app/api/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Report analysis failed."
                );
            }


            console.log(
                "Analysis result:",
                data
            );


            setResult(data);

        } catch (err) {

            console.error(
                "Analysis error:",
                err
            );

            setError(
                err.message ||
                "Something went wrong while analyzing the report."
            );

        } finally {

            setIsAnalyzing(false);
        }
    };


    // =========================================================
    // SEND CHAT MESSAGE
    // =========================================================

    const handleSendMessage = async () => {

        const trimmedQuestion =
            question.trim();

        if (!trimmedQuestion) {
            return;
        }

        if (!result) {

            setError(
                "Please analyze a report before asking questions."
            );

            return;
        }


        const userMessage = {

            role: "user",

            content: trimmedQuestion
        };


        const updatedMessages = [
            ...messages,
            userMessage
        ];


        setMessages(
            updatedMessages
        );

        setQuestion("");

        setError("");

        setIsChatting(true);


        try {

            const response = await fetch(
                "https://backend-pink-five-90.vercel.app/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        report_text:
                            result.report_text || "",

                        results:
                            result.results || [],

                        explanation:
                            result.explanation || {},

                        question:
                            trimmedQuestion,

                        conversation_history:
                            messages
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to get an answer."
                );
            }


            const aiMessage = {

                role: "assistant",

                content:
                    data.answer ||
                    "I couldn't generate an answer."
            };


            setMessages([
                ...updatedMessages,
                aiMessage
            ]);


        } catch (err) {

            console.error(
                "Chat error:",
                err
            );

            setError(
                err.message ||
                "Something went wrong while answering your question."
            );

        } finally {

            setIsChatting(false);
        }
    };


    // =========================================================
    // ENTER KEY
    // =========================================================

    const handleKeyDown = (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            handleSendMessage();
        }
    };


    // =========================================================
    // RESULT COUNTS
    // =========================================================

    const normalResults =
        result?.results?.filter(
            (item) =>
                String(item.status)
                    .toUpperCase() === "NORMAL"
        ) || [];


    const attentionResults =
        result?.results?.filter(
            (item) => {

                const status =
                    String(item.status)
                        .toUpperCase();

                return (
                    status === "LOW" ||
                    status === "HIGH"
                );
            }
        ) || [];


    // =========================================================
    // RENDER
    // =========================================================

    return (

        <div className="dashboard-page">


            {/* ================================================= */}
            {/* HEADER */}
            {/* ================================================= */}

            <header className="dashboard-header">

                <div className="dashboard-logo">

                    <div className="dashboard-logo-icon">
                        ✚
                    </div>

                    <div className="dashboard-logo-text">

                        <span>
                            MedExplain
                        </span>

                        <span className="dashboard-logo-ai">
                            AI
                        </span>

                    </div>

                </div>


                <button
                    className="back-button"
                    onClick={onBack}
                >
                    ← Back to Home
                </button>

            </header>


            {/* ================================================= */}
            {/* MAIN */}
            {/* ================================================= */}

            <main className="dashboard-main">


                {/* ================================================= */}
                {/* REPORT INPUT */}
                {/* ================================================= */}

                <section className="upload-card">


                    <div className="upload-card-heading">

                        <div className="upload-icon">
                            📄
                        </div>

                        <h1>
                            Analyze your medical report
                        </h1>

                        <p>
                            Upload a report or enter its information
                            to start your MedExplain AI session.
                        </p>

                    </div>


                    {/* ================================================= */}
                    {/* TABS */}
                    {/* ================================================= */}

                    <div className="report-tabs">

                        <button
                            className={`report-tab ${activeTab === "pdf"
                                ? "active"
                                : ""
                                }`}
                            onClick={() =>
                                handleTabChange("pdf")
                            }
                        >

                            <span className="tab-icon">
                                📄
                            </span>

                            <span className="tab-text">

                                <strong>
                                    PDF Report
                                </strong>

                                <small>
                                    Upload PDF
                                </small>

                            </span>

                        </button>


                        <button
                            className={`report-tab ${activeTab === "image"
                                ? "active"
                                : ""
                                }`}
                            onClick={() =>
                                handleTabChange("image")
                            }
                        >

                            <span className="tab-icon">
                                🖼️
                            </span>

                            <span className="tab-text">

                                <strong>
                                    Report Image
                                </strong>

                                <small>
                                    Upload photo
                                </small>

                            </span>

                        </button>


                        <button
                            className={`report-tab ${activeTab === "write"
                                ? "active"
                                : ""
                                }`}
                            onClick={() =>
                                handleTabChange("write")
                            }
                        >

                            <span className="tab-icon">
                                ✍️
                            </span>

                            <span className="tab-text">

                                <strong>
                                    Write Report
                                </strong>

                                <small>
                                    Enter manually
                                </small>

                            </span>

                        </button>

                    </div>


                    {/* ================================================= */}
                    {/* PDF */}
                    {/* ================================================= */}

                    {activeTab === "pdf" && (

                        <label className="upload-area">

                            <input
                                type="file"
                                accept=".pdf"
                                onChange={handleFileChange}
                            />

                            <div className="upload-cloud">
                                ☁
                            </div>

                            <strong>
                                Click to choose a PDF report
                            </strong>

                            <span>
                                PDF files only
                            </span>

                        </label>
                    )}


                    {/* ================================================= */}
                    {/* IMAGE */}
                    {/* ================================================= */}

                    {activeTab === "image" && (

                        <label className="upload-area">

                            <input
                                type="file"
                                accept=".png,.jpg,.jpeg"
                                onChange={handleFileChange}
                            />

                            <div className="upload-cloud">
                                🖼️
                            </div>

                            <strong>
                                Click to upload report image
                            </strong>

                            <span>
                                PNG, JPG or JPEG
                            </span>

                        </label>
                    )}


                    {/* ================================================= */}
                    {/* WRITE */}
                    {/* ================================================= */}

                    {activeTab === "write" && (

                        <div className="write-report-container">

                            <div className="write-report-top">

                                <div>

                                    <h3>
                                        Enter your report details
                                    </h3>

                                    <p>
                                        Paste or type the information
                                        from your medical report.
                                    </p>

                                </div>

                                <span className="write-status">
                                    Manual entry
                                </span>

                            </div>


                            <textarea
                                className="write-report-textarea"

                                value={writtenReport}

                                onChange={(event) =>
                                    setWrittenReport(
                                        event.target.value
                                    )
                                }

                                placeholder={`Example:

Hemoglobin: 10.5 g/dL
Reference Range: 12.0 - 16.0

WBC Count: 8500 /uL
Reference Range: 4000 - 11000`}
                            />


                            <div className="textarea-footer">

                                <span>
                                    Your report stays within this analysis session.
                                </span>

                                <span>
                                    {writtenReport.length} characters
                                </span>

                            </div>

                        </div>
                    )}


                    {/* ================================================= */}
                    {/* FILE PREVIEW */}
                    {/* ================================================= */}

                    {file &&
                        activeTab !== "write" && (

                            <div className="selected-file">

                                <div className="selected-file-left">

                                    <div className="selected-file-icon">

                                        {activeTab === "pdf"
                                            ? "📄"
                                            : "🖼️"}

                                    </div>


                                    <div className="selected-file-info">

                                        <strong>
                                            {file.name}
                                        </strong>

                                        <span>
                                            {(file.size / 1024).toFixed(1)}
                                            {" "}KB
                                        </span>

                                    </div>

                                </div>


                                <button
                                    className="remove-file"

                                    onClick={() =>
                                        setFile(null)
                                    }
                                >
                                    ×
                                </button>

                            </div>
                        )}


                    {/* ================================================= */}
                    {/* ANALYZE */}
                    {/* ================================================= */}

                    <button
                        className="analyze-button"

                        disabled={
                            isAnalyzing ||
                            (
                                activeTab !== "write" &&
                                !file
                            ) ||
                            (
                                activeTab === "write" &&
                                !writtenReport.trim()
                            )
                        }

                        onClick={handleAnalyze}
                    >

                        {isAnalyzing ? (

                            <>
                                <span className="loading-spinner"></span>

                                Analyzing your report...
                            </>

                        ) : (

                            <>
                                ✨ Analyze Report
                            </>

                        )}

                    </button>


                    {/* ================================================= */}
                    {/* ERROR */}
                    {/* ================================================= */}

                    {error && (

                        <div className="error-message">
                            ⚠ {error}
                        </div>

                    )}

                </section>


                {/* ================================================= */}
                {/* RESULTS */}
                {/* ================================================= */}

                {result && (

                    <section className="results-section">


                        {/* ================================================= */}
                        {/* INTRO */}
                        {/* ================================================= */}

                        <div className="results-intro">

                            <div>

                                <span className="section-label">
                                    ANALYSIS COMPLETE
                                </span>

                                <h2>
                                    Your report, explained clearly.
                                </h2>

                                <p>
                                    MedExplain AI has analyzed the
                                    information in your report.
                                    You can now ask questions about it
                                    using the AI assistant below.
                                </p>

                            </div>


                            <div className="results-badge">
                                ✨ AI Analysis Complete
                            </div>

                        </div>


                        {/* ================================================= */}
                        {/* STATS */}
                        {/* ================================================= */}

                        <div className="results-stats">

                            <div className="result-stat">

                                <span className="result-stat-icon">
                                    📊
                                </span>

                                <div>

                                    <strong>
                                        {result.results?.length || 0}
                                    </strong>

                                    <span>
                                        Results analyzed
                                    </span>

                                </div>

                            </div>


                            <div className="result-stat">

                                <span className="result-stat-icon">
                                    ✓
                                </span>

                                <div>

                                    <strong>
                                        {normalResults.length}
                                    </strong>

                                    <span>
                                        Within range
                                    </span>

                                </div>

                            </div>


                            <div className="result-stat">

                                <span className="result-stat-icon">
                                    !
                                </span>

                                <div>

                                    <strong>
                                        {attentionResults.length}
                                    </strong>

                                    <span>
                                        Need attention
                                    </span>

                                </div>

                            </div>

                        </div>


                        {/* ================================================= */}
                        {/* AI REPORT EXPLANATION */}
                        {/* ================================================= */}

                        <section className="report-explanation-card">


                            <div className="report-explanation-header">

                                <div className="ai-avatar">
                                    ✨
                                </div>

                                <div>

                                    <h3>
                                        MedExplain AI
                                    </h3>

                                    <p>
                                        Complete explanation of your report
                                    </p>

                                </div>

                            </div>


                            <div className="report-explanation-body">


                                {/* SUMMARY */}

                                {result.summary && (

                                    <div className="explanation-block">

                                        <span className="explanation-label">
                                            OVERVIEW
                                        </span>

                                        <h3>
                                            Overall summary
                                        </h3>

                                        <p>
                                            {result.summary}
                                        </p>

                                    </div>
                                )}


                                {/* KEY FINDINGS */}

                                {result.key_findings?.length > 0 && (

                                    <div className="explanation-block">

                                        <span className="explanation-label">
                                            KEY FINDINGS
                                        </span>

                                        <h3>
                                            What stands out
                                        </h3>

                                        <ul>

                                            {result.key_findings.map(
                                                (finding, index) => (

                                                    <li key={index}>
                                                        {finding}
                                                    </li>

                                                )
                                            )}

                                        </ul>

                                    </div>
                                )}


                                {/* ATTENTION RESULTS */}

                                {attentionResults.length > 0 && (

                                    <div className="explanation-block">

                                        <span className="explanation-label">
                                            RESULTS TO REVIEW
                                        </span>

                                        <h3>
                                            Results outside the reference range
                                        </h3>

                                        <div className="explanation-items">

                                            {attentionResults.map(
                                                (item, index) => (

                                                    <div
                                                        className="explanation-item attention-item"
                                                        key={index}
                                                    >

                                                        <div className="explanation-item-top">

                                                            <strong>
                                                                {item.test}
                                                            </strong>

                                                            <span>
                                                                {String(item.status || "").toUpperCase()}
                                                            </span>

                                                        </div>

                                                        <p>
                                                            Your result is{" "}
                                                            <strong>
                                                                {item.value} {item.unit}
                                                            </strong>
                                                            {" "}while the reported reference range is{" "}
                                                            <strong>
                                                                {item.reference_low} - {item.reference_high} {item.unit}
                                                            </strong>
                                                            .
                                                        </p>

                                                        <p>
                                                            This value is outside the reference range
                                                            provided by the laboratory. A result outside
                                                            a reference range does not by itself establish
                                                            a diagnosis and should be interpreted in context.
                                                        </p>

                                                    </div>

                                                )
                                            )}

                                        </div>

                                    </div>
                                )}


                                {/* NORMAL RESULTS */}

                                {normalResults.length > 0 && (

                                    <div className="explanation-block">

                                        <span className="explanation-label">
                                            WITHIN RANGE
                                        </span>

                                        <h3>
                                            Results within the reference range
                                        </h3>

                                        <div className="explanation-items">

                                            {normalResults.map(
                                                (item, index) => (

                                                    <div
                                                        className="explanation-item normal-item"
                                                        key={index}
                                                    >

                                                        <div className="explanation-item-top">

                                                            <strong>
                                                                {item.test}
                                                            </strong>

                                                            <span>
                                                                NORMAL
                                                            </span>

                                                        </div>

                                                        <p>
                                                            Your result is{" "}
                                                            <strong>
                                                                {item.value} {item.unit}
                                                            </strong>
                                                            {" "}and is within the reported reference range of{" "}
                                                            <strong>
                                                                {item.reference_low} - {item.reference_high} {item.unit}
                                                            </strong>
                                                            .
                                                        </p>

                                                    </div>

                                                )
                                            )}

                                        </div>

                                    </div>
                                )}
                                {/* ================================================= */}
                                {/* MULTI-RESULT PATTERNS */}
                                {/* ================================================= */}

                                {result.patterns?.length > 0 && (

                                    <div className="explanation-block pattern-detection-block">

                                        <span className="explanation-label">
                                            PATTERN DETECTION
                                        </span>

                                        <h3>
                                            Patterns found across your results
                                        </h3>

                                        <p>
                                            MedExplain AI identified the following
                                            combinations of laboratory findings. These are
                                            educational signals and are not diagnoses.
                                        </p>

                                        <div className="explanation-items">

                                            {result.patterns.map(
                                                (pattern, index) => (

                                                    <div
                                                        className="explanation-item pattern-item"
                                                        key={index}
                                                    >

                                                        <div className="explanation-item-top">

                                                            <strong>
                                                                {pattern.pattern}
                                                            </strong>

                                                            <span>
                                                                PATTERN
                                                            </span>

                                                        </div>

                                                        {pattern.related_tests?.length > 0 && (

                                                            <p>
                                                                <strong>
                                                                    Related tests:
                                                                </strong>{" "}

                                                                {pattern.related_tests.join(", ")}
                                                            </p>

                                                        )}

                                                        {pattern.interpretation && (

                                                            <p>
                                                                <strong>
                                                                    What it may mean:
                                                                </strong>{" "}

                                                                {pattern.interpretation}
                                                            </p>

                                                        )}

                                                    </div>
                                                )
                                            )}

                                        </div>

                                    </div>
                                )}


                                {/* MEANING */}

                                {result.meaning && (

                                    <div className="explanation-block">

                                        <span className="explanation-label">
                                            INTERPRETATION
                                        </span>

                                        <h3>
                                            What these results generally mean
                                        </h3>

                                        <p>
                                            {result.meaning}
                                        </p>

                                    </div>
                                )}


                                {/* NEXT STEP */}

                                {result.next_step && (

                                    <div className="explanation-block next-step-block">

                                        <span className="explanation-label">
                                            NEXT STEP
                                        </span>

                                        <h3>
                                            What you may consider doing next
                                        </h3>

                                        <p>
                                            {result.next_step}
                                        </p>

                                    </div>
                                )}

                            </div>

                        </section>


                        {/* ================================================= */}
                        {/* REAL CHATBOT */}
                        {/* ================================================= */}

                        <section className="real-chat-section">


                            {/* CHAT HEADER */}

                            <div className="real-chat-header">

                                <div className="chat-header-left">

                                    <div className="ai-avatar">
                                        ✨
                                    </div>

                                    <div>

                                        <h3>
                                            Ask MedExplain AI
                                        </h3>

                                        <p>
                                            Ask anything about this report
                                        </p>

                                    </div>

                                </div>


                                <div className="online-indicator">

                                    <span></span>

                                    AI ready

                                </div>

                            </div>


                            {/* CHAT MESSAGES */}

                            <div className="real-chat-body">


                                {messages.length === 0 && (

                                    <div className="chat-empty-state">

                                        <div className="chat-empty-icon">
                                            ✨
                                        </div>

                                        <h3>
                                            Ask a question about your report
                                        </h3>

                                        <p>
                                            I can explain your results,
                                            summarize the report, or help
                                            you understand individual values.
                                        </p>


                                        <div className="suggestion-list">

                                            <button
                                                onClick={() =>
                                                    setQuestion(
                                                        "Summarize my report in simple language."
                                                    )
                                                }
                                            >
                                                Summarize my report
                                            </button>

                                            <button
                                                onClick={() =>
                                                    setQuestion(
                                                        "Which results are outside the reference range?"
                                                    )
                                                }
                                            >
                                                Which results need attention?
                                            </button>

                                            <button
                                                onClick={() =>
                                                    setQuestion(
                                                        "Explain my abnormal results in simple language."
                                                    )
                                                }
                                            >
                                                Explain abnormal results
                                            </button>

                                            <button
                                                onClick={() =>
                                                    setQuestion(
                                                        "Explain the most important findings in my report."
                                                    )
                                                }
                                            >
                                                Explain important findings
                                            </button>

                                        </div>

                                    </div>
                                )}


                                {messages.map(
                                    (message, index) => (

                                        <div
                                            className={`chat-message ${message.role === "user"
                                                ? "user-message"
                                                : "ai-message"
                                                }`}
                                            key={index}
                                        >

                                            {message.role === "assistant" && (

                                                <div className="ai-avatar message-avatar">
                                                    ✨
                                                </div>

                                            )}


                                            <div className="message-content">

                                                <span className="message-label">

                                                    {message.role === "user"
                                                        ? "YOU"
                                                        : "MEDEXPLAIN AI"}

                                                </span>


                                                <div className="message-text">

                                                    {cleanAiText(message.content)
                                                        .split("\n")
                                                        .map((line, lineIndex) => (

                                                            <p key={lineIndex}>
                                                                {line || "\u00A0"}
                                                            </p>

                                                        ))}

                                                </div>

                                            </div>


                                            {message.role === "user" && (

                                                <div className="user-avatar">
                                                    You
                                                </div>

                                            )}

                                        </div>
                                    )
                                )}


                                {isChatting && (

                                    <div className="chat-message ai-message">

                                        <div className="ai-avatar message-avatar">
                                            ✨
                                        </div>

                                        <div className="message-content">

                                            <span className="message-label">
                                                MEDEXPLAIN AI
                                            </span>

                                            <div className="typing-indicator">

                                                <span></span>
                                                <span></span>
                                                <span></span>

                                            </div>

                                        </div>

                                    </div>
                                )}

                            </div>


                            {/* CHAT INPUT */}

                            <div className="chat-input-area">

                                <div className="chat-input-wrapper">

                                    <textarea
                                        value={question}

                                        onChange={(event) =>
                                            setQuestion(
                                                event.target.value
                                            )
                                        }

                                        onKeyDown={handleKeyDown}

                                        placeholder="Ask anything about your medical report..."

                                        rows={1}

                                        disabled={isChatting}
                                    />


                                    <button
                                        className="send-button"

                                        onClick={
                                            handleSendMessage
                                        }

                                        disabled={
                                            !question.trim() ||
                                            isChatting
                                        }
                                    >
                                        ↑
                                    </button>

                                </div>


                                <div className="chat-input-footer">

                                    <span>
                                        MedExplain AI answers using
                                        information from your report.
                                    </span>

                                    <span>
                                        Enter to send · Shift + Enter for new line
                                    </span>

                                </div>

                            </div>


                        </section>


                        {/* ================================================= */}
                        {/* LAB TABLE */}
                        {/* ================================================= */}

                        {result.results?.length > 0 && (

                            <section className="lab-results-section">

                                <div className="lab-results-header">

                                    <span className="section-label">
                                        DETAILED RESULTS
                                    </span>

                                    <h3>
                                        Laboratory results
                                    </h3>

                                    <p>
                                        Values extracted from the report
                                        and compared with the provided
                                        reference ranges.
                                    </p>

                                </div>


                                <div className="results-table-wrapper">

                                    <table className="results-table">

                                        <thead>

                                            <tr>

                                                <th>
                                                    Test
                                                </th>

                                                <th>
                                                    Result
                                                </th>

                                                <th>
                                                    Reference Range
                                                </th>

                                                <th>
                                                    Status
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>

                                            {result.results.map(
                                                (item, index) => (

                                                    <tr key={index}>

                                                        <td>
                                                            <strong>
                                                                {item.test}
                                                            </strong>
                                                        </td>

                                                        <td>
                                                            <strong>
                                                                {item.value}
                                                            </strong>{" "}
                                                            {item.unit}
                                                        </td>

                                                        <td>
                                                            {item.reference_low}
                                                            {" - "}
                                                            {item.reference_high}
                                                        </td>

                                                        <td>

                                                            <span
                                                                className={`status-badge ${String(
                                                                    item.status
                                                                ).toLowerCase()}`}
                                                            >
                                                                {item.status}
                                                            </span>

                                                        </td>

                                                    </tr>
                                                )
                                            )}

                                        </tbody>

                                    </table>

                                </div>

                            </section>
                        )}


                        {/* ================================================= */}
                        {/* DISCLAIMER */}
                        {/* ================================================= */}

                        <section className="dashboard-safety">

                            <div className="safety-icon">
                                ♥
                            </div>

                            <div>

                                <h3>
                                    Important medical information
                                </h3>

                                <p>
                                    MedExplain AI explains information
                                    contained in medical reports. It does
                                    not provide a diagnosis and should not
                                    replace advice from a qualified
                                    healthcare professional.
                                </p>

                            </div>

                        </section>

                    </section>
                )}

            </main>

        </div>
    );
}


export default Dashboard;