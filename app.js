function startResearch() {
    const topic = document.getElementById('topicInput').value;
    if (!topic) return;

    // Show loading
    document.getElementById('initialState').style.display = 'none';
    document.getElementById('reportResult').style.display = 'none';
    document.getElementById('loadingState').style.display = 'flex';
    document.getElementById('researchBtn').disabled = true;
    document.getElementById('btnText').innerText = 'Processing...';

    // Simulate AI thinking time
    setTimeout(() => {
        generateMockReport(topic);
    }, 2500);
}

function generateMockReport(topic) {
    const data = {
        "vector database": {
            topic: "Vector Databases",
            summary: "Vector databases are specialized storage engines that handle high-dimensional embeddings. Unlike traditional relational databases, they use semantic similarity to find relationships between data points, making them the backbone of Large Language Model (LLM) applications and Retrieval-Augmented Generation (RAG).",
            keyPoints: [
                "Efficient high-dimensional vector storage.",
                "Fast semantic similarity search via indexing.",
                "Enables memory for LLM agents.",
                "Supports diverse data (text, image, audio).",
                "Scalable to billions of vectors."
            ],
            useCases: [
                "Semantic Document Search",
                "Recommendation Systems",
                "AI Content Moderation"
            ],
            difficulty: "Intermediate",
            nextSteps: "Study vector indexing algorithms like HNSW and IVF, then implement a FAISS-based RAG pipeline."
        },
        "langchain": {
            topic: "LangChain Framework",
            summary: "LangChain is the premier framework for developing applications powered by large language models. It provides a modular set of tools, components, and interfaces that simplify the entire lifecycle of LLM application development, from prompt management to deployment.",
            keyPoints: [
                "Modular chains via LCEL syntax.",
                "Robust tool and agent integration.",
                "Unified API for diverse LLM providers.",
                "Comprehensive logging and observability.",
                "Large ecosystem of community integrations."
            ],
            useCases: [
                "Autonomous AI Researchers",
                "Complex Customer Support Bots",
                "Data Analysis Copilots"
            ],
            difficulty: "Beginner",
            nextSteps: "Master the LCEL pipe syntax and explore LangGraph for stateful agentic workflows."
        }
    };

    // Default to general info if not found in mock data
    const report = data[topic.toLowerCase()] || {
        topic: topic,
        summary: `${topic} is a significant technical domain in the 2025 AI landscape, focusing on specialized computational patterns and intelligent orchestration.`,
        keyPoints: [
            "Critical component of modern AI stacks.",
            "Enables advanced reasoning capabilities.",
            "Scalable architecture patterns.",
            "Rapidly evolving community ecosystem.",
            "Standardized integration interfaces."
        ],
        useCases: [
            "Enterprise Automation",
            "Technical Problem Solving",
            "Predictive Maintenance"
        ],
        difficulty: "Advanced",
        nextSteps: "Review the official documentation and build a minimal prototype to test edge cases."
    };

    // Update UI
    document.getElementById('resTopic').innerText = report.topic.toUpperCase();
    document.getElementById('resSummary').innerText = report.summary;
    document.getElementById('resDifficulty').innerText = report.difficulty;
    document.getElementById('resNextSteps').innerText = report.nextSteps;

    const kpCont = document.getElementById('resKeyPoints');
    kpCont.innerHTML = report.keyPoints.map(kp => `<div class="list-item"><i class="fas fa-chevron-right"></i> ${kp}</div>`).join('');

    const ucCont = document.getElementById('resUseCases');
    ucCont.innerHTML = report.useCases.map(uc => `<div class="list-item"><i class="fas fa-check"></i> ${uc}</div>`).join('');

    // Switch screens
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('reportResult').style.display = 'block';
    document.getElementById('researchBtn').disabled = false;
    document.getElementById('btnText').innerText = 'Execute Research';
}
