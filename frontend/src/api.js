// api.js

/**
 * Simulates a RAG API call to the backend.
 *
 * @param {string} query The user's input query.
 * @returns {Promise<{text: string, sources: Array<string>}>}
 */
export const getChatResponse = async (query) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Simple context-based response for demo
    let response = {
        text: "Thank you for your query. The current literature on **Type 2 Diabetes Mellitus (T2DM)** emphasizes a multifaceted approach combining lifestyle modification and pharmacological intervention [1]. Recent studies suggest that **SGLT-2 inhibitors** show promise not only for glycemic control but also for cardiovascular and renal protection, making them a preferred second-line agent for patients with established cardiovascular disease [2]. If the patient is non-responsive to metformin and has no cardiovascular risk, **DPP-4 inhibitors** remain a safe and effective option [1].",
        sources: [
            { title: "WHO Guidelines on Hypertension Management, 2023" },
            { title: "JAMA Article on ACE Inhibitor Efficacy" }
        ]
    };

    if (query.toLowerCase().includes('cardiovascular')) {
        response.text = "Regarding **cardiovascular disease risk stratification**, the European Society of Cardiology guidelines recommend using the SCORE2 risk calculation tool [1]. Primary prevention strategies focus heavily on aggressive management of **hypertension and hyperlipidemia**, often targeting an LDL cholesterol reduction of over 50% [2]. Novel therapies like **PCSK9 inhibitors** are reserved for high-risk patients who fail to achieve targets on maximum tolerated statin therapy [1].";
        response.sources = [
            { title: "SCORE2 Risk Assessment Documentation" },
            { title: "ESC Guidelines on Hyperlipidemia, 2023" }
        ];
    }
    
    return response;
};
