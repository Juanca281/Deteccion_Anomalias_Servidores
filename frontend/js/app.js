// ============================================================
// SERVIDORIA
// FRONTEND PRINCIPAL
// ============================================================


// ============================================================
// REFERENCIAS GENERALES
// ============================================================

const sidebar =
    document.getElementById("sidebar");

const menuToggle =
    document.getElementById("menuToggle");

const pageTitle =
    document.getElementById("pageTitle");

const sections =
    document.querySelectorAll(
        ".content-section"
    );

const navItems =
    document.querySelectorAll(
        ".nav-item"
    );


// ============================================================
// TÍTULOS DE NAVEGACIÓN
// ============================================================

const sectionTitles = {
    inicio: "Inicio",
    semana2: "Semana 2",
    semana3: "Semana 3",
    semana4: "Semana 4",
    semana5: "Semana 5",
    semana7: "Semana 7",
    arquitectura: "Arquitectura"
};


// ============================================================
// CAMBIAR DE SECCIÓN
// ============================================================

function showSection(sectionId) {

    const targetSection =
        document.getElementById(
            sectionId
        );


    if (!targetSection) {
        return;
    }


    sections.forEach(section => {

        section.classList.remove(
            "active-section"
        );

    });


    targetSection.classList.add(
        "active-section"
    );


    navItems.forEach(item => {

        item.classList.remove(
            "active"
        );


        if (
            item.dataset.section
            === sectionId
        ) {

            item.classList.add(
                "active"
            );

        }

    });


    if (pageTitle) {

        pageTitle.textContent =
            sectionTitles[sectionId]
            || "ServidorIA";

    }


    history.replaceState(
        null,
        "",
        `#${sectionId}`
    );


    if (
        window.innerWidth <= 760
        && sidebar
    ) {

        sidebar.classList.remove(
            "open"
        );

    }


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// ============================================================
// EVENTOS DE NAVEGACIÓN
// ============================================================

navItems.forEach(item => {

    item.addEventListener(
        "click",
        () => {

            showSection(
                item.dataset.section
            );

        }
    );

});


// ============================================================
// MENÚ MÓVIL
// ============================================================

if (
    menuToggle
    && sidebar
) {

    menuToggle.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            sidebar.classList.toggle(
                "open"
            );

        }
    );

}


document.addEventListener(
    "click",
    event => {

        if (
            window.innerWidth > 760
            || !sidebar
            || !menuToggle
        ) {

            return;

        }


        if (
            !sidebar.contains(
                event.target
            )
            && !menuToggle.contains(
                event.target
            )
        ) {

            sidebar.classList.remove(
                "open"
            );

        }

    }
);


// ============================================================
// CARGA INICIAL
// ============================================================

function loadInitialSection() {

    const hash =
        window.location.hash
            .replace("#", "");


    if (
        hash
        && document.getElementById(hash)
    ) {

        showSection(hash);

        return;

    }


    showSection(
        "semana7"
    );

}


// ============================================================
// EJECUTAR SEMANAS 2, 3, 4 Y 5
// ============================================================

async function runScript(
    scriptName,
    outputId
) {

    const output =
        document.getElementById(
            outputId
        );


    if (!output) {
        return;
    }


    output.textContent =
        "Ejecutando programa...";


    try {

        const response =
            await fetch(
                `/api/run/${scriptName}`,
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error
                || "No fue posible ejecutar el programa."
            );

        }


        let text = "";


        if (data.stdout) {

            text +=
                data.stdout;

        }


        if (data.stderr) {

            if (text) {
                text += "\n\n";
            }


            text +=
                "ERROR:\n"
                + data.stderr;

        }


        text +=
            "\n\n"
            + "----------------------------------------\n";


        text +=
            data.success
                ? "Estado: ejecución correcta"
                : "Estado: ejecución con errores";


        output.textContent =
            text;


    } catch (error) {

        output.textContent =
            "Error al ejecutar el programa:\n\n"
            + error.message;

    }

}


// ============================================================
// CARGAR ARCHIVOS
// ============================================================

async function loadFile(
    path,
    viewerId
) {

    const viewer =
        document.getElementById(
            viewerId
        );


    if (!viewer) {
        return;
    }


    if (
        !viewer.classList.contains(
            "hidden"
        )
        && viewer.dataset.loaded
        === path
    ) {

        viewer.classList.add(
            "hidden"
        );

        return;

    }


    viewer.classList.remove(
        "hidden"
    );


    viewer.textContent =
        "Cargando archivo...";


    try {

        const response =
            await fetch(
                `/project/${path}?t=${Date.now()}`
            );


        if (!response.ok) {

            let message =
                "No fue posible cargar el archivo.";


            try {

                const data =
                    await response.json();


                if (data.error) {

                    message =
                        data.error;

                }

            } catch {
                // Respuesta no JSON
            }


            throw new Error(
                message
            );

        }


        const content =
            await response.text();


        viewer.textContent =
            content;


        viewer.dataset.loaded =
            path;


    } catch (error) {

        viewer.textContent =
            "Error al cargar el archivo:\n\n"
            + error.message;

    }

}


// ============================================================
// REFRESCAR ARCHIVO ABIERTO
// ============================================================

async function refreshFile(
    path,
    viewerId
) {

    const viewer =
        document.getElementById(
            viewerId
        );


    if (
        !viewer
        || viewer.classList.contains(
            "hidden"
        )
    ) {

        return;

    }


    try {

        const response =
            await fetch(
                `/project/${path}?t=${Date.now()}`
            );


        if (!response.ok) {
            return;
        }


        viewer.textContent =
            await response.text();


        viewer.dataset.loaded =
            path;


    } catch {
        // El análisis continúa aunque
        // falle la actualización.
    }

}


// ============================================================
// SEMANA 7
// EJEMPLOS
// ============================================================

const semana7Examples = {

    normal: [

        {
            cpu: 42,
            ram: 50,
            disco: 58,
            latencia: 38,
            solicitudes: 460,
            errores: 0,
            estado: "Activo"
        },

        {
            cpu: 46,
            ram: 53,
            disco: 60,
            latencia: 41,
            solicitudes: 490,
            errores: 0,
            estado: "Activo"
        },

        {
            cpu: 48,
            ram: 55,
            disco: 62,
            latencia: 45,
            solicitudes: 510,
            errores: 1,
            estado: "Activo"
        }

    ],


    degradacion: [

        {
            cpu: 45,
            ram: 52,
            disco: 61,
            latencia: 40,
            solicitudes: 470,
            errores: 0,
            estado: "Activo"
        },

        {
            cpu: 83,
            ram: 74,
            disco: 65,
            latencia: 90,
            solicitudes: 720,
            errores: 2,
            estado: "Activo"
        },

        {
            cpu: 94,
            ram: 91,
            disco: 94,
            latencia: 260,
            solicitudes: 1600,
            errores: 18,
            estado: "Activo"
        },

        {
            cpu: 96,
            ram: 93,
            disco: 95,
            latencia: 290,
            solicitudes: 1700,
            errores: 24,
            estado: "Activo"
        }

    ],


    recuperacion: [

        {
            cpu: 45,
            ram: 52,
            disco: 61,
            latencia: 40,
            solicitudes: 470,
            errores: 0,
            estado: "Activo"
        },

        {
            cpu: 83,
            ram: 74,
            disco: 65,
            latencia: 90,
            solicitudes: 720,
            errores: 2,
            estado: "Activo"
        },

        {
            cpu: 94,
            ram: 91,
            disco: 94,
            latencia: 260,
            solicitudes: 1600,
            errores: 18,
            estado: "Activo"
        },

        {
            cpu: 96,
            ram: 93,
            disco: 95,
            latencia: 290,
            solicitudes: 1700,
            errores: 24,
            estado: "Activo"
        },

        {
            cpu: 55,
            ram: 61,
            disco: 70,
            latencia: 62,
            solicitudes: 530,
            errores: 1,
            estado: "Activo"
        },

        {
            cpu: 48,
            ram: 57,
            disco: 68,
            latencia: 45,
            solicitudes: 500,
            errores: 0,
            estado: "Activo"
        }

    ]

};


// ============================================================
// AGREGAR NUEVA LECTURA
// ============================================================

function addObservation(
    values = null
) {

    const container =
        document.getElementById(
            "observationsContainer"
        );


    if (!container) {
        return;
    }


    const index =
        container.querySelectorAll(
            ".observation-card"
        ).length;


    const observation = {
        cpu:
            values?.cpu ?? 50,

        ram:
            values?.ram ?? 55,

        disco:
            values?.disco ?? 60,

        latencia:
            values?.latencia ?? 50,

        solicitudes:
            values?.solicitudes ?? 500,

        errores:
            values?.errores ?? 0,

        estado:
            values?.estado ?? "Activo"
    };


    const article =
        document.createElement(
            "article"
        );


    article.className =
        "observation-card";


    article.dataset.observationIndex =
        index;


    article.innerHTML = `
        <div class="observation-header">

            <div>

                <span class="observation-number">
                    ${String(index + 1).padStart(2, "0")}
                </span>

                <strong>
                    Lectura del servidor
                </strong>

            </div>

            <button
                class="button button-secondary remove-observation"
                type="button"
                title="Eliminar lectura"
            >
                Eliminar
            </button>

        </div>


        <div class="telemetry-grid">

            <div class="form-group">

                <label>
                    CPU
                </label>

                <div class="input-unit">

                    <input
                        class="obs-cpu"
                        type="number"
                        min="0"
                        max="100"
                        value="${observation.cpu}"
                    >

                    <span>
                        %
                    </span>

                </div>

            </div>


            <div class="form-group">

                <label>
                    Memoria RAM
                </label>

                <div class="input-unit">

                    <input
                        class="obs-ram"
                        type="number"
                        min="0"
                        max="100"
                        value="${observation.ram}"
                    >

                    <span>
                        %
                    </span>

                </div>

            </div>


            <div class="form-group">

                <label>
                    Disco
                </label>

                <div class="input-unit">

                    <input
                        class="obs-disco"
                        type="number"
                        min="0"
                        max="100"
                        value="${observation.disco}"
                    >

                    <span>
                        %
                    </span>

                </div>

            </div>


            <div class="form-group">

                <label>
                    Latencia
                </label>

                <div class="input-unit">

                    <input
                        class="obs-latencia"
                        type="number"
                        min="0"
                        value="${observation.latencia}"
                    >

                    <span>
                        ms
                    </span>

                </div>

            </div>


            <div class="form-group">

                <label>
                    Solicitudes / minuto
                </label>

                <input
                    class="obs-solicitudes"
                    type="number"
                    min="0"
                    value="${observation.solicitudes}"
                >

            </div>


            <div class="form-group">

                <label>
                    Errores
                </label>

                <input
                    class="obs-errores"
                    type="number"
                    min="0"
                    value="${observation.errores}"
                >

            </div>


            <div class="form-group">

                <label>
                    Estado
                </label>

                <select class="obs-estado">

                    <option
                        value="Activo"
                        ${
                            observation.estado === "Activo"
                                ? "selected"
                                : ""
                        }
                    >
                        Activo
                    </option>

                    <option
                        value="Inactivo"
                        ${
                            observation.estado === "Inactivo"
                                ? "selected"
                                : ""
                        }
                    >
                        Inactivo
                    </option>

                    <option
                        value="Mantenimiento"
                        ${
                            observation.estado === "Mantenimiento"
                                ? "selected"
                                : ""
                        }
                    >
                        Mantenimiento
                    </option>

                </select>

            </div>

        </div>
    `;


    const removeButton =
        article.querySelector(
            ".remove-observation"
        );


    removeButton.addEventListener(
        "click",
        () => {

            removeObservation(
                article
            );

        }
    );


    container.appendChild(
        article
    );


    renumberObservations();

}


// ============================================================
// ELIMINAR LECTURA
// ============================================================

function removeObservation(
    card
) {

    const container =
        document.getElementById(
            "observationsContainer"
        );


    if (!container) {
        return;
    }


    const cards =
        container.querySelectorAll(
            ".observation-card"
        );


    if (
        cards.length <= 1
    ) {

        showAnalysisMessage(
            "Debe existir al menos una lectura del servidor."
        );

        return;

    }


    card.remove();


    renumberObservations();

}


// ============================================================
// RENUMERAR LECTURAS
// ============================================================

function renumberObservations() {

    const cards =
        document.querySelectorAll(
            "#observationsContainer .observation-card"
        );


    cards.forEach(
        (
            card,
            index
        ) => {

            card.dataset.observationIndex =
                index;


            const number =
                card.querySelector(
                    ".observation-number"
                );


            if (number) {

                number.textContent =
                    String(
                        index + 1
                    ).padStart(
                        2,
                        "0"
                    );

            }

        }
    );

}


// ============================================================
// LIMPIAR LECTURAS
// ============================================================

function clearObservations() {

    const container =
        document.getElementById(
            "observationsContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML =
        "";

}


// ============================================================
// CARGAR EJEMPLO
// ============================================================

function loadSemana7Example(
    type
) {

    const example =
        semana7Examples[type];


    if (!example) {
        return;
    }


    clearObservations();


    example.forEach(
        observation => {

            addObservation(
                observation
            );

        }
    );


    resetAnalysisResults();

}


// ============================================================
// LEER TODAS LAS OBSERVACIONES
// ============================================================

function getObservations() {

    const cards =
        document.querySelectorAll(
            "#observationsContainer .observation-card"
        );


    const observations =
        [];


    cards.forEach(card => {

        observations.push({

            cpu:
                Number(
                    card.querySelector(
                        ".obs-cpu"
                    ).value
                ),

            ram:
                Number(
                    card.querySelector(
                        ".obs-ram"
                    ).value
                ),

            disco:
                Number(
                    card.querySelector(
                        ".obs-disco"
                    ).value
                ),

            latencia:
                Number(
                    card.querySelector(
                        ".obs-latencia"
                    ).value
                ),

            solicitudes:
                Number(
                    card.querySelector(
                        ".obs-solicitudes"
                    ).value
                ),

            errores:
                Number(
                    card.querySelector(
                        ".obs-errores"
                    ).value
                ),

            estado:
                card.querySelector(
                    ".obs-estado"
                ).value

        });

    });


    return observations;

}


// ============================================================
// VALIDAR OBSERVACIONES
// ============================================================

function validateObservations(
    observations
) {

    if (
        observations.length === 0
    ) {

        return (
            "Debe existir al menos una lectura."
        );

    }


    for (
        let i = 0;
        i < observations.length;
        i++
    ) {

        const data =
            observations[i];


        const prefix =
            `Lectura ${i + 1}: `;


        if (
            !Number.isFinite(data.cpu)
            || data.cpu < 0
            || data.cpu > 100
        ) {

            return (
                prefix
                + "CPU debe estar entre 0 y 100."
            );

        }


        if (
            !Number.isFinite(data.ram)
            || data.ram < 0
            || data.ram > 100
        ) {

            return (
                prefix
                + "RAM debe estar entre 0 y 100."
            );

        }


        if (
            !Number.isFinite(data.disco)
            || data.disco < 0
            || data.disco > 100
        ) {

            return (
                prefix
                + "Disco debe estar entre 0 y 100."
            );

        }


        if (
            !Number.isFinite(data.latencia)
            || data.latencia < 0
        ) {

            return (
                prefix
                + "la latencia no puede ser negativa."
            );

        }


        if (
            !Number.isFinite(data.solicitudes)
            || data.solicitudes < 0
        ) {

            return (
                prefix
                + "las solicitudes no pueden ser negativas."
            );

        }


        if (
            !Number.isFinite(data.errores)
            || data.errores < 0
        ) {

            return (
                prefix
                + "los errores no pueden ser negativos."
            );

        }

    }


    return null;

}


// ============================================================
// EJECUTAR SEMANA 7
// ============================================================

async function runSemana7() {

    const observations =
        getObservations();


    const validationError =
        validateObservations(
            observations
        );


    if (
        validationError
    ) {

        showAnalysisMessage(
            validationError
        );

        return;

    }


    const button =
        document.getElementById(
            "analyzeButton"
        );


    setAnalysisLoading(
        button,
        true
    );


    try {

        const response =
            await fetch(
                "/api/semana7",
                {

                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            observaciones:
                                observations
                        })

                }
            );


        const data =
            await response.json();


        if (
            !response.ok
        ) {

            throw new Error(
                data.error
                || "No fue posible realizar el análisis."
            );

        }


        if (
            data.success === false
        ) {

            throw new Error(
                data.error
                || data.stderr
                || "El análisis presentó un error."
            );

        }


        // ----------------------------------------------------
        // Permite varias estructuras de respuesta del backend
        // ----------------------------------------------------

        let analysis =
            data.analysis
            || data.result
            || null;


        // ----------------------------------------------------
        // Si Flask devuelve el JSON generado por Python
        // dentro de stdout, también lo interpretamos.
        // ----------------------------------------------------

        if (
            !analysis
            && data.stdout
        ) {

            try {

                analysis =
                    JSON.parse(
                        data.stdout
                    );

            } catch {

                analysis =
                    null;

            }

        }


        // ----------------------------------------------------
        // Si el backend devuelve directamente el análisis.
        // ----------------------------------------------------

        if (
            !analysis
            && data.observations
            && data.automaton
        ) {

            analysis =
                data;

        }


        if (!analysis) {

            throw new Error(
                "El backend no devolvió "
                + "los datos estructurados del análisis."
            );

        }


        renderSemana7Analysis(
            analysis
        );


        await refreshFile(
            "reports/semana07.md",
            "viewer-semana7"
        );


    } catch (error) {

        showAnalysisMessage(
            error.message
        );

    } finally {

        setAnalysisLoading(
            button,
            false
        );

    }

}


// ============================================================
// ESTADO DE CARGA
// ============================================================

function setAnalysisLoading(
    button,
    loading
) {

    if (!button) {
        return;
    }


    if (loading) {

        button.disabled =
            true;


        button.dataset.originalText =
            button.textContent;


        button.textContent =
            "Analizando comportamiento...";


        button.style.opacity =
            "0.7";


        button.style.cursor =
            "wait";

    } else {

        button.disabled =
            false;


        button.textContent =
            button.dataset.originalText
            || "Analizar comportamiento";


        button.style.opacity =
            "";


        button.style.cursor =
            "";

    }

}


// ============================================================
// MOSTRAR RESULTADOS SEMANA 7
// ============================================================

function renderSemana7Analysis(
    analysis
) {

    const empty =
        document.getElementById(
            "analysisEmpty"
        );


    const dashboard =
        document.getElementById(
            "analysisDashboard"
        );


    if (empty) {

        empty.classList.add(
            "hidden"
        );

    }


    if (dashboard) {

        dashboard.classList.remove(
            "hidden"
        );

    }


    const readings =
        analysis.observations
        || [];


    if (
        readings.length === 0
    ) {

        showAnalysisMessage(
            "No se recibieron lecturas analizadas."
        );

        return;

    }


    const lastReading =
        readings[
            readings.length - 1
        ];


    const lastData =
        lastReading.data
        || {};


    // ========================================================
    // ÚLTIMA LECTURA
    // ========================================================

    setText(
        "resultCpu",
        `${formatNumber(lastData.cpu)}%`
    );


    setText(
        "resultRam",
        `${formatNumber(lastData.ram)}%`
    );


    setText(
        "resultDisk",
        `${formatNumber(lastData.disco)}%`
    );


    setText(
        "resultLatency",
        `${formatNumber(lastData.latencia)} ms`
    );


    setText(
        "resultRequests",
        formatInteger(
            lastData.solicitudes
        )
    );


    setText(
        "resultErrors",
        formatInteger(
            lastData.errores
        )
    );


    setText(
        "resultServerStatus",
        lastData.estado
        || "-"
    );


    const distance =
        lastReading.numeric?.distance
        ?? 0;


    setText(
        "numericDistance",
        Number(distance)
            .toFixed(4)
    );


    // ========================================================
    // BARRAS
    // ========================================================

    updateMetricBar(
        "barCpu",
        lastData.cpu,
        80
    );


    updateMetricBar(
        "barRam",
        lastData.ram,
        85
    );


    updateMetricBar(
        "barDisk",
        lastData.disco,
        90
    );


    const latencyVisual =
        Math.min(
            (
                Number(
                    lastData.latencia
                )
                / 300
            )
            * 100,
            100
        );


    updateMetricBar(
        "barLatency",
        latencyVisual,
        50
    );


    // ========================================================
    // CLASIFICACIÓN AUTOMÁTICA
    // ========================================================

    renderClassificationTimeline(
        readings
    );


    // ========================================================
    // REPRESENTACIÓN SIMBÓLICA
    // ========================================================

    renderSymbolicAnalysis(
        readings
    );


    // ========================================================
    // SECUENCIA
    // ========================================================

    setText(
        "generatedSequence",
        analysis.sequence
        || "-"
    );


    // ========================================================
    // AUTÓMATA
    // ========================================================

    renderAutomata(
        analysis.automaton
    );


    // ========================================================
    // PATRONES
    // ========================================================

    renderPatterns(
        analysis.patterns
        || []
    );


    // ========================================================
    // ESTADO GENERAL
    // ========================================================

    renderGeneralStatus(
        analysis
    );

}


// ============================================================
// CLASIFICACIÓN DE LECTURAS
// ============================================================

function renderClassificationTimeline(
    readings
) {

    const container =
        document.getElementById(
            "classificationTimeline"
        );


    if (!container) {
        return;
    }


    container.innerHTML =
        "";


    readings.forEach(
        (
            reading,
            index
        ) => {

            const classification =
                reading.classification
                || {};


            const symbol =
                classification.symbol
                || "?";


            const state =
                getSymbolInfo(
                    symbol
                );


            const item =
                document.createElement(
                    "div"
                );


            item.className =
                `classification-item ${state.className}`;


            item.innerHTML = `
                <strong>
                    ${state.name}
                </strong>

                <small>
                    Lectura ${index + 1}
                    · ${symbol}
                </small>
            `;


            container.appendChild(
                item
            );


            if (
                index
                < readings.length - 1
            ) {

                const arrow =
                    document.createElement(
                        "div"
                    );


                arrow.className =
                    "process-arrow";


                arrow.textContent =
                    "→";


                container.appendChild(
                    arrow
                );

            }

        }
    );

}


// ============================================================
// REPRESENTACIÓN SIMBÓLICA
// ============================================================

function renderSymbolicAnalysis(
    readings
) {

    const factsContainer =
        document.getElementById(
            "symbolicFacts"
        );


    const conclusionsContainer =
        document.getElementById(
            "symbolicConclusions"
        );


    if (
        !factsContainer
        || !conclusionsContainer
    ) {

        return;

    }


    factsContainer.innerHTML =
        "";


    conclusionsContainer.innerHTML =
        "";


    const uniqueFacts =
        new Set();


    const uniqueConclusions =
        new Set();


    readings.forEach(reading => {

        const symbolic =
            reading.symbolic
            || {};


        (
            symbolic.facts
            || []
        ).forEach(
            fact => {

                uniqueFacts.add(
                    fact
                );

            }
        );


        (
            symbolic.conclusions
            || []
        ).forEach(
            conclusion => {

                uniqueConclusions.add(
                    conclusion
                );

            }
        );

    });


    uniqueFacts.forEach(
        fact => {

            const element =
                document.createElement(
                    "span"
                );


            element.className =
                "fact-badge";


            if (
                fact.includes(
                    "critico"
                )
                || fact.includes(
                    "errores_altos"
                )
                || fact.includes(
                    "servidor_no_disponible"
                )
            ) {

                element.classList.add(
                    "critical"
                );

            } else if (
                fact.includes(
                    "alta"
                )
                || fact.includes(
                    "altos"
                )
            ) {

                element.classList.add(
                    "warning"
                );

            }


            element.textContent =
                formatLabel(
                    fact
                );


            factsContainer.appendChild(
                element
            );

        }
    );


    uniqueConclusions.forEach(
        conclusion => {

            const element =
                document.createElement(
                    "span"
                );


            element.className =
                "conclusion-tag";


            element.textContent =
                formatLabel(
                    conclusion
                );


            conclusionsContainer.appendChild(
                element
            );

        }
    );

}


// ============================================================
// AUTÓMATA VISUAL
// ============================================================

function renderAutomata(
    automaton
) {

    const container =
        document.getElementById(
            "automataVisual"
        );


    if (!container) {
        return;
    }


    if (
        !automaton
        || !Array.isArray(
            automaton.trace
        )
    ) {

        container.innerHTML = `
            <div class="analysis-placeholder">
                No se recibió información
                del autómata.
            </div>
        `;

        return;

    }


    container.innerHTML =
        "";


    const track =
        document.createElement(
            "div"
        );


    track.className =
        "automata-track";


    // ========================================================
    // ESTADO INICIAL
    // ========================================================

    track.appendChild(
        createAutomataState(
            "q0",
            "NORMAL",
            "Inicio"
        )
    );


    // ========================================================
    // TRANSICIONES
    // ========================================================

    automaton.trace.forEach(
        item => {

            const arrow =
                document.createElement(
                    "div"
                );


            arrow.className =
                "automata-arrow";


            arrow.innerHTML = `
                <span title="Entrada ${item.symbol}">
                    →
                </span>
            `;


            track.appendChild(
                arrow
            );


            track.appendChild(
                createAutomataState(
                    item.to,
                    item.to_name,
                    `Entrada ${item.symbol}`
                )
            );

        }
    );


    container.appendChild(
        track
    );


    setText(
        "automataFinalState",
        `${automaton.final_state} · ${automaton.final_name}`
    );

}


// ============================================================
// CREAR ESTADO VISUAL
// ============================================================

function createAutomataState(
    state,
    name,
    detail
) {

    const div =
        document.createElement(
            "div"
        );


    const className =
        getAutomataClass(
            state
        );


    div.className =
        `automata-state ${className}`;


    div.innerHTML = `
        <strong>
            ${name}
        </strong>

        <small>
            ${state} · ${detail}
        </small>
    `;


    return div;

}


// ============================================================
// CLASE SEGÚN ESTADO DEL AUTÓMATA
// ============================================================

function getAutomataClass(
    state
) {

    const classes = {
        q0: "normal",
        q1: "alerta",
        q2: "alerta",
        q3: "critico",
        q4: "recuperacion"
    };


    return (
        classes[state]
        || "normal"
    );

}


// ============================================================
// INFORMACIÓN DE SÍMBOLOS
// ============================================================

function getSymbolInfo(
    symbol
) {

    const states = {

        N: {
            name: "NORMAL",
            className: "normal"
        },

        A: {
            name: "ADVERTENCIA",
            className: "alert"
        },

        C: {
            name: "CRÍTICO",
            className: "critical"
        },

        R: {
            name: "RECUPERACIÓN",
            className: "recovery"
        }

    };


    return (
        states[symbol]
        || {
            name: "DESCONOCIDO",
            className: "normal"
        }
    );

}


// ============================================================
// PATRONES RECONOCIDOS
// ============================================================

function renderPatterns(
    patterns
) {

    const container =
        document.getElementById(
            "patternsContainer"
        );


    if (!container) {
        return;
    }


    container.innerHTML =
        "";


    if (
        patterns.length === 0
    ) {

        const card =
            document.createElement(
                "article"
            );


        card.className =
            "pattern-card";


        card.innerHTML = `
            <span>
                PATRÓN
            </span>

            <strong>
                Sin patrón identificado
            </strong>

            <p>
                No se reconoció un patrón
                temporal específico.
            </p>
        `;


        container.appendChild(
            card
        );


        return;

    }


    patterns.forEach(
        pattern => {

            const card =
                document.createElement(
                    "article"
                );


            card.className =
                "pattern-card";


            card.innerHTML = `
                <span>
                    PATRÓN RECONOCIDO
                </span>

                <strong>
                    ${pattern.name}
                </strong>

                <p>
                    ${pattern.description}
                </p>
            `;


            container.appendChild(
                card
            );

        }
    );

}


// ============================================================
// ESTADO GENERAL
// ============================================================

function renderGeneralStatus(
    analysis
) {

    const automaton =
        analysis.automaton
        || {};


    const finalState =
        automaton.final_state
        || "q0";


    let status =
        "NORMAL";


    let badge =
        "Operación normal";


    let badgeClass =
        "status-normal";


    if (
        finalState === "q1"
    ) {

        status =
            "ADVERTENCIA";


        badge =
            "Requiere observación";


        badgeClass =
            "status-alert";

    }


    if (
        finalState === "q2"
    ) {

        status =
            "ANOMALÍA";


        badge =
            "Anomalía persistente";


        badgeClass =
            "status-alert";

    }


    if (
        finalState === "q3"
    ) {

        status =
            "CRÍTICO";


        badge =
            "Atención requerida";


        badgeClass =
            "status-critical";

    }


    if (
        finalState === "q4"
    ) {

        status =
            "RECUPERACIÓN";


        badge =
            "En recuperación";


        badgeClass =
            "status-recovery";

    }


    setText(
        "analysisStatus",
        status
    );


    setText(
        "analysisDescription",
        analysis.final_description
        || ""
    );


    const badgeElement =
        document.getElementById(
            "analysisStatusBadge"
        );


    if (badgeElement) {

        badgeElement.className =
            `result-status ${badgeClass}`;


        badgeElement.textContent =
            badge;

    }


    // ========================================================
    // CONCLUSIÓN FINAL
    // ========================================================

    const patterns =
        analysis.patterns
        || [];


    if (
        patterns.length > 0
    ) {

        setText(
            "analysisConclusion",
            patterns[0].name
        );

    } else {

        setText(
            "analysisConclusion",
            status
        );

    }


    setText(
        "finalStateDescription",
        analysis.final_description
        || ""
    );

}


// ============================================================
// BARRAS DE MÉTRICAS
// ============================================================

function updateMetricBar(
    id,
    value,
    criticalLimit
) {

    const bar =
        document.getElementById(
            id
        );


    if (!bar) {
        return;
    }


    const percentage =
        Math.max(
            0,
            Math.min(
                Number(value) || 0,
                100
            )
        );


    bar.style.width =
        `${percentage}%`;


    bar.classList.remove(
        "warning",
        "critical"
    );


    if (
        percentage >= criticalLimit
    ) {

        bar.classList.add(
            "critical"
        );

        return;

    }


    if (
        percentage
        >= criticalLimit * 0.8
    ) {

        bar.classList.add(
            "warning"
        );

    }

}


// ============================================================
// RESETEAR RESULTADOS
// ============================================================

function resetAnalysisResults() {

    const empty =
        document.getElementById(
            "analysisEmpty"
        );


    const dashboard =
        document.getElementById(
            "analysisDashboard"
        );


    if (empty) {

        empty.classList.remove(
            "hidden"
        );

    }


    if (dashboard) {

        dashboard.classList.add(
            "hidden"
        );

    }

}


// ============================================================
// MOSTRAR ERROR DE ANÁLISIS
// ============================================================

function showAnalysisMessage(
    message
) {

    const empty =
        document.getElementById(
            "analysisEmpty"
        );


    const dashboard =
        document.getElementById(
            "analysisDashboard"
        );


    if (dashboard) {

        dashboard.classList.add(
            "hidden"
        );

    }


    if (!empty) {

        alert(message);

        return;

    }


    empty.classList.remove(
        "hidden"
    );


    empty.innerHTML = `
        <div class="placeholder-icon">
            !
        </div>

        <strong>
            No se pudo realizar el análisis
        </strong>

        <p>
            ${escapeHtml(message)}
        </p>
    `;

}


// ============================================================
// FORMATEAR ETIQUETAS PYTHON
// ============================================================

function formatLabel(
    text
) {

    if (!text) {
        return "";
    }


    const formatted =
        String(text)
            .replace(
                /_/g,
                " "
            )
            .trim();


    return (
        formatted.charAt(0)
            .toUpperCase()
        + formatted.slice(1)
    );

}


// ============================================================
// FORMATEAR NÚMEROS
// ============================================================

function formatNumber(
    value
) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "0";

    }


    if (
        Number.isInteger(number)
    ) {

        return number.toString();

    }


    return number.toFixed(1);

}


function formatInteger(
    value
) {

    const number =
        Number(value);


    if (
        !Number.isFinite(number)
    ) {

        return "0";

    }


    return Math.round(number)
        .toLocaleString(
            "es-CO"
        );

}


// ============================================================
// TEXTO SEGURO
// ============================================================

function escapeHtml(
    text
) {

    return String(
        text
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}


// ============================================================
// UTILIDAD PARA CAMBIAR TEXTO
// ============================================================

function setText(
    id,
    value
) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.textContent =
            value;

    }

}


// ============================================================
// VALIDACIÓN VISUAL DE PORCENTAJES
// ============================================================

document.addEventListener(
    "change",
    event => {

        if (
            !event.target.matches(
                ".obs-cpu, .obs-ram, .obs-disco"
            )
        ) {

            return;

        }


        let value =
            Number(
                event.target.value
            );


        if (
            !Number.isFinite(value)
        ) {

            value = 0;

        }


        value =
            Math.max(
                0,
                Math.min(
                    value,
                    100
                )
            );


        event.target.value =
            value;

    }
);


// ============================================================
// ESTADO DEL BACKEND
// ============================================================

async function checkBackend() {

    const topbarStatus =
        document.querySelector(
            ".topbar-status"
        );


    const sidebarStatus =
        document.querySelector(
            ".sidebar-status"
        );


    try {

        const response =
            await fetch(
                "/api/status"
            );


        if (!response.ok) {

            throw new Error();

        }


        if (topbarStatus) {

            topbarStatus.innerHTML = `
                <span
                    class="status-indicator"
                ></span>

                <span>
                    Backend conectado
                </span>
            `;

        }


        if (sidebarStatus) {

            sidebarStatus.innerHTML = `
                <span
                    class="status-dot"
                ></span>

                <div>

                    <strong>
                        Sistema disponible
                    </strong>

                    <small>
                        Semana 7
                    </small>

                </div>
            `;

        }


    } catch {

        if (topbarStatus) {

            topbarStatus.innerHTML = `
                <span
                    class="status-indicator"
                    style="background:#bf4545;"
                ></span>

                <span>
                    Backend no disponible
                </span>
            `;

        }


        if (sidebarStatus) {

            sidebarStatus.innerHTML = `
                <span
                    class="status-dot"
                    style="background:#bf4545;"
                ></span>

                <div>

                    <strong>
                        Sin conexión
                    </strong>

                    <small>
                        Revisar Flask
                    </small>

                </div>
            `;

        }

    }

}


// ============================================================
// PREPARAR PRIMERA LECTURA
// ============================================================

function initializeFirstObservation() {

    const firstCard =
        document.querySelector(
            "#observationsContainer .observation-card"
        );


    if (!firstCard) {

        addObservation();

        return;

    }


    renumberObservations();

}


// ============================================================
// INICIALIZACIÓN
// ============================================================

function initializeApp() {

    loadInitialSection();

    initializeFirstObservation();

    resetAnalysisResults();

    checkBackend();

}


// ============================================================
// INICIO
// ============================================================

initializeApp();