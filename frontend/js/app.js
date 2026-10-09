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
    semana8: "Semana 8 - Reconocimiento neuronal y ontología",
    semana9: "Semana 9 - Reconocimiento y procesamiento de imágenes",
    semana10: "Semana 10 - Análisis físico mediante visión artificial",
    arquitectura: "Arquitectura"
};


// ============================================================
// UTILIDADES DE IMÁGENES
// ============================================================

const MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024;

function validateImageFile(file) {
    if (!file) {
        return "No se recibió ningún archivo.";
    }

    const extension = file.name
        .split(".")
        .pop()
        .toLowerCase();

    const validExtension = ["png", "jpg", "jpeg"].includes(extension);
    const validType = !file.type || ["image/png", "image/jpeg"].includes(file.type);

    if (!validExtension || !validType) {
        return "Solo se permiten imágenes PNG, JPG o JPEG.";
    }

    if (file.size > MAX_IMAGE_SIZE_BYTES) {
        return "La imagen supera el tamaño máximo de 10 MB.";
    }

    return null;
}

function setupImageDropArea(areaId, inputId, onFile) {
    const area = document.getElementById(areaId);
    const input = document.getElementById(inputId);

    if (!area || !input) {
        return;
    }

    area.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            input.click();
        }
    });

    ["dragenter", "dragover"].forEach(eventName => {
        area.addEventListener(eventName, event => {
            event.preventDefault();
            area.classList.add("is-dragging");
        });
    });

    ["dragleave", "drop"].forEach(eventName => {
        area.addEventListener(eventName, event => {
            event.preventDefault();
            area.classList.remove("is-dragging");
        });
    });

    area.addEventListener("drop", event => {
        const file = event.dataTransfer?.files?.[0];

        if (file) {
            onFile(file);
        }
    });
}


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
        "semana10"
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
                        Semana 10
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


// ============================================================
// SEMANA 8
// Reconocimiento neuronal + SQLite + Ontología
// ============================================================

let semana8SelectedFile = null;
let semana8PreviewUrl = null;


// ============================================================
// ABRIR SELECTOR
// ============================================================

function openSemana8File() {

    document
        .getElementById("semana8ImageInput")
        .click();
}


// ============================================================
// ESCUCHAR ARCHIVO
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input = document.getElementById(
            "semana8ImageInput"
        );

        if (!input) {
            return;
        }


        input.addEventListener(
            "change",
            (event) => {

                const file =
                    event.target.files[0];

                if (!file) {
                    return;
                }

                selectSemana8Image(
                    file
                );
            }
        );

        setupImageDropArea(
            "semana8UploadArea",
            "semana8ImageInput",
            selectSemana8Image
        );

    }
);


// ============================================================
// SELECCIONAR IMAGEN
// ============================================================

function selectSemana8Image(file) {

    const validationError =
        validateImageFile(file);

    if (validationError) {
        showSemana8Error(validationError);
        return;
    }


    semana8SelectedFile = file;


    // --------------------------------------------------------
    // Eliminar URL anterior
    // --------------------------------------------------------

    if (semana8PreviewUrl) {

        URL.revokeObjectURL(
            semana8PreviewUrl
        );
    }


    semana8PreviewUrl =
        URL.createObjectURL(
            file
        );


    // --------------------------------------------------------
    // Vista previa
    // --------------------------------------------------------

    const preview =
        document.getElementById(
            "semana8Preview"
        );


    preview.src =
        semana8PreviewUrl;

    preview.hidden = false;


    document.getElementById(
        "semana8UploadEmpty"
    ).hidden = true;


    document.getElementById(
        "semana8FileInfo"
    ).hidden = false;


    document.getElementById(
        "semana8FileName"
    ).textContent =
        file.name;


    document.getElementById(
        "semana8AnalyzeButton"
    ).disabled = false;


    // Limpiar estados anteriores

    document.getElementById(
        "semana8Error"
    ).hidden = true;


    document.getElementById(
        "semana8Results"
    ).hidden = true;
}


// ============================================================
// QUITAR IMAGEN
// ============================================================

function clearSemana8Image() {

    semana8SelectedFile = null;


    const input =
        document.getElementById(
            "semana8ImageInput"
        );


    input.value = "";


    if (semana8PreviewUrl) {

        URL.revokeObjectURL(
            semana8PreviewUrl
        );

        semana8PreviewUrl = null;
    }


    const preview =
        document.getElementById(
            "semana8Preview"
        );


    preview.src = "";
    preview.hidden = true;


    document.getElementById(
        "semana8UploadEmpty"
    ).hidden = false;


    document.getElementById(
        "semana8FileInfo"
    ).hidden = true;


    document.getElementById(
        "semana8AnalyzeButton"
    ).disabled = true;


    document.getElementById(
        "semana8Results"
    ).hidden = true;


    resetSemana8Status();
}


// ============================================================
// EJECUTAR ANÁLISIS
// ============================================================

async function runSemana8() {

    if (!semana8SelectedFile) {

        showSemana8Error(
            "Selecciona una imagen antes de analizar."
        );

        return;
    }


    const button =
        document.getElementById(
            "semana8AnalyzeButton"
        );


    button.disabled = true;

    button.textContent =
        "Analizando...";


    // --------------------------------------------------------
    // Estado visual
    // --------------------------------------------------------

    document.getElementById(
        "semana8InitialState"
    ).hidden = true;


    document.getElementById(
        "semana8Loading"
    ).hidden = false;


    document.getElementById(
        "semana8Error"
    ).hidden = true;


    document.getElementById(
        "semana8Results"
    ).hidden = true;


    try {

        const formData =
            new FormData();


        formData.append(
            "imagen",
            semana8SelectedFile
        );


        const response =
            await fetch(
                "/api/semana8",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "No fue posible realizar el análisis."
            );
        }


        renderSemana8Result(
            data
        );

    }

    catch (error) {

        showSemana8Error(
            error.message
        );

    }

    finally {

        document.getElementById(
            "semana8Loading"
        ).hidden = true;


        button.disabled = false;

        button.textContent =
            "Analizar imagen";
    }
}


// ============================================================
// RENDERIZAR RESULTADO
// ============================================================

function renderSemana8Result(data) {

    const prediction =
        data.prediction || {};


    const evidence =
        data.evidence || {};


    const ontology =
        data.ontology || {};


    // ========================================================
    // PREDICCIÓN
    // ========================================================

    document.getElementById(
        "semana8Prediction"
    ).textContent =
        prediction.class || "-";


    const confidence =
        Number(
            prediction.confidence || 0
        );


    document.getElementById(
        "semana8ConfidenceValue"
    ).textContent =
        `${confidence.toFixed(2)}%`;


    document.getElementById(
        "semana8ConfidenceText"
    ).textContent =
        `El modelo asignó una confianza de ${confidence.toFixed(2)}%.`;


    document.getElementById(
        "semana8ConfidenceBar"
    ).style.width =
        `${Math.min(confidence, 100)}%`;


    // ========================================================
    // NIVEL DE CONFIANZA
    // ========================================================

    const level =
        prediction.confidence_level ||
        "-";


    const badge =
        document.getElementById(
            "semana8ConfidenceBadge"
        );


    badge.textContent =
        level;


    badge.className =
        "semana8-confidence-badge";


    const normalized =
        level
            .toLowerCase()
            .normalize("NFD")
            .replace(
                /[\u0300-\u036f]/g,
                ""
            )
            .replace(
                /\s+/g,
                "-"
            );


    if (
        normalized === "confiable"
    ) {

        badge.classList.add(
            "confiable"
        );

    }

    else if (
        normalized === "moderada"
    ) {

        badge.classList.add(
            "moderada"
        );

    }

    else {

        badge.classList.add(
            "no-concluyente"
        );
    }


    // ========================================================
    // PROBABILIDADES
    // ========================================================

    renderSemana8Probabilities(
        prediction.probabilities || {}
    );


    // ========================================================
    // SQLITE
    // ========================================================

    document.getElementById(
        "semana8EvidenceId"
    ).textContent =
        evidence.id ?? "-";


    document.getElementById(
        "semana8EvidenceDate"
    ).textContent =
        evidence.date || "-";


    document.getElementById(
        "semana8EvidenceDatabase"
    ).textContent =
        evidence.database ||
        "artifacts/imagenes.db";


    // ========================================================
    // ONTOLOGÍA
    // ========================================================

    document.getElementById(
        "semana8OntologyConcept"
    ).textContent =
        ontology.concept || "-";


    document.getElementById(
        "semana8OntologyType"
    ).textContent =
        ontology.type || "-";


    document.getElementById(
        "semana8Interpretation"
    ).textContent =
        ontology.interpretation || "-";


    document.getElementById(
        "semana8OntologyGraph"
    ).textContent =
        ontology.graph ||
        "artifacts/ontologia.graphml";


    renderSemana8Metrics(
        ontology.affected_metrics || []
    );


    // ========================================================
    // MOSTRAR RESULTADOS
    // ========================================================

    document.getElementById(
        "semana8InitialState"
    ).hidden = true;


    document.getElementById(
        "semana8Error"
    ).hidden = true;


    const results = document.getElementById(
        "semana8Results"
    );

    results.hidden = false;
    results.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================================
// PROBABILIDADES
// ============================================================

function renderSemana8Probabilities(
    probabilities
) {

    const container =
        document.getElementById(
            "semana8Probabilities"
        );


    container.innerHTML = "";


    const ordered =
        Object.entries(
            probabilities
        )
        .sort(
            (
                [, valueA],
                [, valueB]
            ) => valueB - valueA
        );


    ordered.forEach(
        (
            [
                className,
                probability
            ]
        ) => {

            const value =
                Number(
                    probability
                );


            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "semana8-probability-row";


            const name =
                document.createElement(
                    "span"
                );


            name.className =
                "semana8-probability-name";

            name.textContent =
                className;


            const track =
                document.createElement(
                    "div"
                );


            track.className =
                "semana8-probability-track";


            const fill =
                document.createElement(
                    "div"
                );


            fill.className =
                "semana8-probability-fill";

            fill.style.width =
                `${Math.min(value, 100)}%`;


            track.appendChild(
                fill
            );


            const percentage =
                document.createElement(
                    "strong"
                );


            percentage.className =
                "semana8-probability-value";

            percentage.textContent =
                `${value.toFixed(2)}%`;


            row.appendChild(
                name
            );

            row.appendChild(
                track
            );

            row.appendChild(
                percentage
            );


            container.appendChild(
                row
            );
        }
    );
}


// ============================================================
// MÉTRICAS AFECTADAS
// ============================================================

function renderSemana8Metrics(
    metrics
) {

    const container =
        document.getElementById(
            "semana8AffectedMetrics"
        );


    container.innerHTML = "";


    if (!metrics.length) {

        const chip =
            document.createElement(
                "span"
            );


        chip.className =
            "semana8-metric-chip";

        chip.textContent =
            "Ninguna";


        container.appendChild(
            chip
        );

        return;
    }


    metrics.forEach(
        metric => {

            const chip =
                document.createElement(
                    "span"
                );


            chip.className =
                "semana8-metric-chip";

            chip.textContent =
                metric;


            container.appendChild(
                chip
            );
        }
    );
}


// ============================================================
// ERROR
// ============================================================

function showSemana8Error(
    message
) {

    document.getElementById(
        "semana8InitialState"
    ).hidden = true;


    document.getElementById(
        "semana8Loading"
    ).hidden = true;


    document.getElementById(
        "semana8Results"
    ).hidden = true;


    document.getElementById(
        "semana8Error"
    ).hidden = false;


    document.getElementById(
        "semana8ErrorText"
    ).textContent =
        message;
}


// ============================================================
// RESTABLECER ESTADO
// ============================================================

function resetSemana8Status() {

    document.getElementById(
        "semana8InitialState"
    ).hidden = false;


    document.getElementById(
        "semana8Loading"
    ).hidden = true;


    document.getElementById(
        "semana8Error"
    ).hidden = true;
}
    // ============================================================
// SEMANA 9
// Canny + Otsu + Regiones conectadas
// ============================================================

let semana9SelectedFile = null;
let semana9PreviewUrl = null;


// ============================================================
// ABRIR SELECTOR
// ============================================================

function openSemana9File() {

    document
        .getElementById(
            "semana9ImageInput"
        )
        .click();
}


// ============================================================
// INICIALIZAR INPUT
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input =
            document.getElementById(
                "semana9ImageInput"
            );


        if (!input) {
            return;
        }


        input.addEventListener(
            "change",
            event => {

                const file =
                    event.target.files[0];


                if (!file) {
                    return;
                }


                selectSemana9Image(
                    file
                );
            }
        );

        setupImageDropArea(
            "semana9UploadArea",
            "semana9ImageInput",
            selectSemana9Image
        );

    }
);


// ============================================================
// SELECCIONAR IMAGEN
// ============================================================

function selectSemana9Image(file) {

    const validationError =
        validateImageFile(file);

    if (validationError) {
        showSemana9Error(validationError);
        return;
    }


    semana9SelectedFile =
        file;


    if (semana9PreviewUrl) {

        URL.revokeObjectURL(
            semana9PreviewUrl
        );
    }


    semana9PreviewUrl =
        URL.createObjectURL(
            file
        );


    const preview =
        document.getElementById(
            "semana9Preview"
        );


    preview.src =
        semana9PreviewUrl;

    preview.hidden =
        false;


    document.getElementById(
        "semana9UploadEmpty"
    ).hidden =
        true;


    document.getElementById(
        "semana9FileInfo"
    ).hidden =
        false;


    document.getElementById(
        "semana9FileName"
    ).textContent =
        file.name;


    document.getElementById(
        "semana9AnalyzeButton"
    ).disabled =
        false;


    document.getElementById(
        "semana9Results"
    ).hidden =
        true;


    document.getElementById(
        "semana9Error"
    ).hidden =
        true;
}


// ============================================================
// QUITAR IMAGEN
// ============================================================

function clearSemana9Image() {

    semana9SelectedFile =
        null;


    const input =
        document.getElementById(
            "semana9ImageInput"
        );


    input.value = "";


    if (semana9PreviewUrl) {

        URL.revokeObjectURL(
            semana9PreviewUrl
        );

        semana9PreviewUrl =
            null;
    }


    const preview =
        document.getElementById(
            "semana9Preview"
        );


    preview.src = "";
    preview.hidden = true;


    document.getElementById(
        "semana9UploadEmpty"
    ).hidden =
        false;


    document.getElementById(
        "semana9FileInfo"
    ).hidden =
        true;


    document.getElementById(
        "semana9AnalyzeButton"
    ).disabled =
        true;


    document.getElementById(
        "semana9Results"
    ).hidden =
        true;


    document.getElementById(
        "semana9Loading"
    ).hidden =
        true;


    document.getElementById(
        "semana9Error"
    ).hidden =
        true;
}


// ============================================================
// EJECUTAR SEMANA 9
// ============================================================

async function runSemana9() {

    if (!semana9SelectedFile) {

        showSemana9Error(
            "Selecciona una imagen antes de procesarla."
        );

        return;
    }


    const sigma =
        Number(
            document
                .getElementById(
                    "semana9Sigma"
                )
                .value
        );


    const minArea =
        Number(
            document
                .getElementById(
                    "semana9MinArea"
                )
                .value
        );


    // ========================================================
    // VALIDACIONES
    // ========================================================

    if (
        !Number.isFinite(sigma)
        ||
        sigma <= 0
    ) {

        showSemana9Error(
            "Sigma debe ser mayor que 0."
        );

        return;
    }


    if (
        !Number.isInteger(minArea)
        ||
        minArea < 1
    ) {

        showSemana9Error(
            "El área mínima debe ser un entero mayor que 0."
        );

        return;
    }


    const button =
        document.getElementById(
            "semana9AnalyzeButton"
        );


    button.disabled =
        true;

    button.textContent =
        "Procesando...";


    document.getElementById(
        "semana9Loading"
    ).hidden =
        false;


    document.getElementById(
        "semana9Error"
    ).hidden =
        true;


    document.getElementById(
        "semana9Results"
    ).hidden =
        true;


    try {

        // ====================================================
        // FORMULARIO
        // ====================================================

        const formData =
            new FormData();


        formData.append(
            "imagen",
            semana9SelectedFile
        );


        formData.append(
            "sigma",
            sigma
        );


        formData.append(
            "min_area",
            minArea
        );


        // ====================================================
        // API
        // ====================================================

        const response =
            await fetch(
                "/api/semana9",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (
            !response.ok
            ||
            !data.success
        ) {

            throw new Error(
                data.error
                ||
                "No se pudo completar el procesamiento."
            );
        }


        renderSemana9Result(
            data
        );

    }

    catch (error) {

        showSemana9Error(
            error.message
        );

    }

    finally {

        document.getElementById(
            "semana9Loading"
        ).hidden =
            true;


        button.disabled =
            false;


        button.textContent =
            "Procesar imagen";
    }
}


// ============================================================
// MOSTRAR RESULTADOS
// ============================================================

function renderSemana9Result(data) {

    const canny =
        data.canny || {};


    const otsu =
        data.otsu || {};


    const regions =
        data.regions || {};


    // ========================================================
    // CANNY
    // ========================================================

    renderSemana9Sigma(
        canny.comparison || []
    );


    // ========================================================
    // OTSU
    // ========================================================

    document.getElementById(
        "semana9Threshold01"
    ).textContent =
        Number(
            otsu.threshold_01 || 0
        ).toFixed(4);


    document.getElementById(
        "semana9Threshold255"
    ).textContent =
        Number(
            otsu.threshold_255 || 0
        ).toFixed(2);


    // ========================================================
    // REGIONES
    // ========================================================

    document.getElementById(
        "semana9TotalRegions"
    ).textContent =
        regions.total ?? "-";


    document.getElementById(
        "semana9RelevantRegions"
    ).textContent =
        regions.relevant ?? "-";


    document.getElementById(
        "semana9MinimumArea"
    ).textContent =
        `${regions.minimum_area ?? "-"} px`;


    // ========================================================
    // TABLA
    // ========================================================

    renderSemana9Regions(
        regions.largest || []
    );

    // ========================================================
    // EVIDENCIAS VISUALES
    // ========================================================

    renderSemana9Evidence(
    data.artifacts || {}
    );

    // ========================================================
    // RESULTADOS
    // ========================================================

    document.getElementById(
        "semana9Error"
    ).hidden =
        true;


    const results = document.getElementById(
        "semana9Results"
    );

    results.hidden = false;
    results.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================================
// COMPARACIÓN SIGMA
// ============================================================

function renderSemana9Sigma(
    comparison
) {

    const container =
        document.getElementById(
            "semana9SigmaResults"
        );


    container.innerHTML = "";


    if (!comparison.length) {

        container.textContent =
            "No existen resultados.";

        return;
    }


    const maximum =
        Math.max(
            ...comparison.map(
                item =>
                    Number(
                        item.edge_pixels
                    )
            )
        );


    comparison.forEach(
        item => {

            const sigma =
                Number(
                    item.sigma
                );


            const pixels =
                Number(
                    item.edge_pixels
                );


            const percentage =
                Number(
                    item.edge_percentage
                );


            const relativeWidth =
                maximum > 0
                    ? pixels / maximum * 100
                    : 0;


            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "semana9-sigma-row";


            const label =
                document.createElement(
                    "span"
                );


            label.className =
                "semana9-sigma-label";


            label.textContent =
                `σ ${sigma.toFixed(1)}`;


            const track =
                document.createElement(
                    "div"
                );


            track.className =
                "semana9-sigma-track";


            const fill =
                document.createElement(
                    "div"
                );


            fill.className =
                "semana9-sigma-fill";


            fill.style.width =
                `${relativeWidth}%`;


            track.appendChild(
                fill
            );


            const value =
                document.createElement(
                    "span"
                );


            value.className =
                "semana9-sigma-value";


            value.textContent =
                `${pixels.toLocaleString()} px · ${percentage.toFixed(2)}%`;


            row.appendChild(
                label
            );


            row.appendChild(
                track
            );


            row.appendChild(
                value
            );


            container.appendChild(
                row
            );
        }
    );
}


// ============================================================
// TABLA REGIONES
// ============================================================

function renderSemana9Regions(
    regions
) {

    const tbody =
        document.getElementById(
            "semana9RegionsTable"
        );


    tbody.innerHTML = "";


    regions.forEach(
        region => {

            const row =
                document.createElement(
                    "tr"
                );


            const values = [
                region.label,
                region.area,
                region.height,
                region.width
            ];


            values.forEach(
                value => {

                    const cell =
                        document.createElement(
                            "td"
                        );


                    cell.textContent =
                        value;


                    row.appendChild(
                        cell
                    );
                }
            );


            tbody.appendChild(
                row
            );
        }
    );
}


// ============================================================
// ERROR
// ============================================================

function showSemana9Error(
    message
) {

    document.getElementById(
        "semana9Loading"
    ).hidden =
        true;


    document.getElementById(
        "semana9Results"
    ).hidden =
        true;


    document.getElementById(
        "semana9Error"
    ).hidden =
        false;


    document.getElementById(
        "semana9ErrorText"
    ).textContent =
        message;
}


// ============================================================
// EVIDENCIAS VISUALES - SEMANA 9
// ============================================================

function renderSemana9Evidence(artifacts) {

    // Evita que el navegador reutilice
    // imágenes antiguas almacenadas en caché.

    const timestamp = Date.now();


    const vision =
        document.getElementById(
            "semana9EvidenceVision"
        );


    const sigma =
        document.getElementById(
            "semana9EvidenceSigma"
        );


    const regions =
        document.getElementById(
            "semana9EvidenceRegions"
        );


    // ========================================================
    // PROCESAMIENTO PRINCIPAL
    // Original + Canny + Otsu
    // ========================================================

    if (
        artifacts.vision
        &&
        vision
    ) {

        vision.src =
            "/" +
            artifacts.vision +
            "?v=" +
            timestamp;
    }


    // ========================================================
    // COMPARACIÓN DE SIGMA
    // ========================================================

    if (
        artifacts.sigma_comparison
        &&
        sigma
    ) {

        sigma.src =
            "/" +
            artifacts.sigma_comparison +
            "?v=" +
            timestamp;
    }


    // ========================================================
    // REGIONES CONECTADAS
    // ========================================================

    if (
        artifacts.regions
        &&
        regions
    ) {

        regions.src =
            "/" +
            artifacts.regions +
            "?v=" +
            timestamp;
    }
}

// ============================================================
// SEMANA 10
// Histogramas + Otsu + Regiones + LBP
// ============================================================

let semana10SelectedFile = null;
let semana10PreviewUrl = null;

let semana10Visuals = {
    original: null,
    gris: null,
    otsu: null,
    lbp: null
};


let semana10LocalVisualData = null;


// ============================================================
// INICIALIZACIÓN
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input =
            document.getElementById(
                "semana10ImageInput"
            );

        if (!input) {
            return;
        }

        input.addEventListener(
            "change",
            event => {

                const file =
                    event.target.files?.[0];

                if (file) {
                    selectSemana10Image(
                        file
                    );
                }

            }
        );

        setupImageDropArea(
            "semana10UploadArea",
            "semana10ImageInput",
            selectSemana10Image
        );

        resetSemana10ProcessViewer();

    }
);


// ============================================================
// ABRIR SELECTOR
// ============================================================

function openSemana10File() {

    const input =
        document.getElementById(
            "semana10ImageInput"
        );

    input?.click();

}


// ============================================================
// SELECCIONAR IMAGEN
// ============================================================

async function selectSemana10Image(file) {

    const validationError =
        validateImageFile(
            file
        );

    if (validationError) {

        showSemana10Error(
            validationError
        );

        return;
    }


    semana10SelectedFile =
        file;


    if (semana10PreviewUrl) {

        URL.revokeObjectURL(
            semana10PreviewUrl
        );

    }


    semana10PreviewUrl =
        URL.createObjectURL(
            file
        );


    semana10Visuals = {
        original:
            semana10PreviewUrl,

        gris:
            null,

        otsu:
            null,

        lbp:
            null
    };


    const preview =
        document.getElementById(
            "semana10Preview"
        );


    if (preview) {

        preview.src =
            semana10PreviewUrl;

        preview.hidden =
            false;

    }


    setHidden(
        "semana10UploadEmpty",
        true
    );

    setHidden(
        "semana10FileInfo",
        false
    );

    setHidden(
        "semana10Results",
        true
    );

    setHidden(
        "semana10Error",
        true
    );


    setText(
        "semana10FileName",
        file.name
    );


    const button =
        document.getElementById(
            "semana10AnalyzeButton"
        );


    if (button) {

        button.disabled =
            false;

    }


    showSemana10Process(
        "original"
    );


    try {

        const localVisuals =
            await buildSemana10LocalVisuals(
                file
            );


        if (
            semana10SelectedFile
            !== file
        ) {

            return;
        }


        semana10Visuals.gris =
            localVisuals.gris;

        semana10Visuals.otsu =
            localVisuals.otsu;

        semana10Visuals.lbp =
            localVisuals.lbp;

        semana10LocalVisualData =
            localVisuals.source;


    } catch {

        // La vista original continúa disponible
        // aunque falle la previsualización local.

    }

}


// ============================================================
// QUITAR IMAGEN
// ============================================================

function clearSemana10Image() {

    semana10SelectedFile =
        null;


    const input =
        document.getElementById(
            "semana10ImageInput"
        );


    if (input) {
        input.value = "";
    }


    if (semana10PreviewUrl) {

        URL.revokeObjectURL(
            semana10PreviewUrl
        );

        semana10PreviewUrl =
            null;

    }


    semana10Visuals = {
        original: null,
        gris: null,
        otsu: null,
        lbp: null
    };


    semana10LocalVisualData =
        null;


    const preview =
        document.getElementById(
            "semana10Preview"
        );


    if (preview) {

        preview.src = "";
        preview.hidden = true;

    }


    setHidden(
        "semana10UploadEmpty",
        false
    );

    setHidden(
        "semana10FileInfo",
        true
    );

    setHidden(
        "semana10Results",
        true
    );

    setHidden(
        "semana10Error",
        true
    );


    const button =
        document.getElementById(
            "semana10AnalyzeButton"
        );


    if (button) {

        button.disabled =
            true;

    }


    resetSemana10ProcessViewer();

}


// ============================================================
// VISOR DE PROCESAMIENTO
// ============================================================

function resetSemana10ProcessViewer() {

    const image =
        document.getElementById(
            "semana10ProcessImage"
        );

    const empty =
        document.getElementById(
            "semana10ProcessEmpty"
        );


    if (image) {

        image.src = "";
        image.hidden = true;

    }


    if (empty) {

        empty.hidden = false;

        empty.innerHTML = `
            <div class="semana10-process-empty-icon">
                ◫
            </div>

            <strong>
                Esperando una fotografía
            </strong>

            <span>
                Carga una imagen para visualizar el procesamiento.
            </span>
        `;

    }


    updateSemana10ProcessTabs(
        "original"
    );


    setText(
        "semana10ProcessTitle",
        "Fotografía original"
    );

    setText(
        "semana10ProcessStage",
        "Entrada"
    );

    setText(
        "semana10ProcessDescription",
        "La imagen seleccionada aparecerá aquí antes del análisis."
    );

}


function normalizeSemana10ArtifactUrl(
    value
) {

    if (!value) {
        return null;
    }


    const url =
        String(value);


    if (
        url.startsWith("http://")
        || url.startsWith("https://")
        || url.startsWith("/")
        || url.startsWith("blob:")
        || url.startsWith("data:")
    ) {

        return url;

    }


    return "/" + url;

}


function updateSemana10ProcessTabs(
    activeType
) {

    const tabMap = {
        original:
            "semana10TabOriginal",

        gris:
            "semana10TabGray",

        otsu:
            "semana10TabOtsu",

        lbp:
            "semana10TabLbp"
    };


    Object.entries(
        tabMap
    ).forEach(
        ([type, id]) => {

            const tab =
                document.getElementById(
                    id
                );


            if (!tab) {
                return;
            }


            const isActive =
                type === activeType;


            tab.classList.toggle(
                "active",
                isActive
            );


            tab.setAttribute(
                "aria-selected",
                String(
                    isActive
                )
            );

        }
    );

}


function showSemana10Process(
    type
) {

    const descriptions = {

        original: {
            title:
                "Fotografía original",

            stage:
                "Entrada",

            text:
                "Imagen seleccionada por el usuario antes del procesamiento."
        },

        gris: {
            title:
                "Escala de grises",

            stage:
                "Intensidad",

            text:
                "Reduce la imagen a niveles de intensidad para facilitar el análisis numérico."
        },

        otsu: {
            title:
                "Segmentación Otsu",

            stage:
                "Segmentación",

            text:
                "Separa automáticamente grupos de píxeles según el umbral de intensidad calculado."
        },

        lbp: {
            title:
                "Textura LBP",

            stage:
                "Textura",

            text:
                "Representa patrones locales de textura utilizados para comparar la superficie con las referencias."
        }

    };


    const information =
        descriptions[type]
        || descriptions.original;


    updateSemana10ProcessTabs(
        type
    );


    setText(
        "semana10ProcessTitle",
        information.title
    );

    setText(
        "semana10ProcessStage",
        information.stage
    );

    setText(
        "semana10ProcessDescription",
        information.text
    );


    const image =
        document.getElementById(
            "semana10ProcessImage"
        );

    const empty =
        document.getElementById(
            "semana10ProcessEmpty"
        );


    if (
        !image
        || !empty
    ) {

        return;
    }


    const url =
        semana10Visuals[type];


    if (!url) {

        image.hidden =
            true;

        empty.hidden =
            false;


        empty.innerHTML = `
            <div class="semana10-process-empty-icon">
                ◫
            </div>

            <strong>
                Vista aún no disponible
            </strong>

            <span>
                Ejecuta el análisis para generar esta etapa visual.
            </span>
        `;


        return;
    }


    const cacheSeparator =
        url.includes("?")
            ? "&"
            : "?";


    const isLocalImage =
        url.startsWith("blob:")
        || url.startsWith("data:");


    image.onload = () => {

        image.hidden =
            false;

        empty.hidden =
            true;

    };


    image.onerror = () => {

        image.hidden =
            true;

        empty.hidden =
            false;

        empty.innerHTML = `
            <div class="semana10-process-empty-icon">
                !
            </div>

            <strong>
                No fue posible mostrar esta vista
            </strong>

            <span>
                Vuelve a seleccionar la fotografía o ejecuta nuevamente el análisis.
            </span>
        `;

    };


    image.src =
        isLocalImage
            ? url
            : `${url}${cacheSeparator}v=${Date.now()}`;

}


// ============================================================
// PREVISUALIZACIONES LOCALES
// Solo se usan para mostrar el procesamiento en el frontend.
// El análisis y las métricas finales siguen viniendo de Python.
// ============================================================

async function loadSemana10ImageSource(file) {

    if ("createImageBitmap" in window) {
        return await createImageBitmap(file);
    }

    return await new Promise((resolve, reject) => {

        const url =
            URL.createObjectURL(file);

        const image =
            new Image();

        image.onload = () => {

            URL.revokeObjectURL(url);
            resolve(image);

        };

        image.onerror = () => {

            URL.revokeObjectURL(url);

            reject(
                new Error(
                    "No fue posible leer la imagen."
                )
            );

        };

        image.src = url;

    });

}


function createSemana10Canvas(width, height) {

    const canvas =
        document.createElement(
            "canvas"
        );

    canvas.width = width;
    canvas.height = height;

    return canvas;

}


function createSemana10GrayValues(imageData) {

    const source =
        imageData.data;

    const totalPixels =
        imageData.width
        * imageData.height;

    const gray =
        new Uint8ClampedArray(
            totalPixels
        );

    for (
        let pixel = 0;
        pixel < totalPixels;
        pixel++
    ) {

        const offset =
            pixel * 4;

        gray[pixel] =
            Math.round(
                source[offset] * 0.2125
                + source[offset + 1] * 0.7154
                + source[offset + 2] * 0.0721
            );

    }

    return gray;

}


function semana10GrayToDataUrl(
    gray,
    width,
    height
) {

    const canvas =
        createSemana10Canvas(
            width,
            height
        );

    const context =
        canvas.getContext(
            "2d"
        );

    const output =
        context.createImageData(
            width,
            height
        );

    for (
        let pixel = 0;
        pixel < gray.length;
        pixel++
    ) {

        const offset =
            pixel * 4;

        const value =
            gray[pixel];

        output.data[offset] = value;
        output.data[offset + 1] = value;
        output.data[offset + 2] = value;
        output.data[offset + 3] = 255;

    }

    context.putImageData(
        output,
        0,
        0
    );

    return canvas.toDataURL(
        "image/png"
    );

}


function calculateSemana10OtsuThreshold(gray) {

    const histogram =
        new Uint32Array(
            256
        );

    for (
        let i = 0;
        i < gray.length;
        i++
    ) {

        histogram[gray[i]]++;

    }

    const total =
        gray.length;

    let weightedTotal = 0;

    for (
        let value = 0;
        value < 256;
        value++
    ) {

        weightedTotal +=
            value
            * histogram[value];

    }

    let backgroundWeight = 0;
    let backgroundSum = 0;
    let maximumVariance = -1;
    let threshold = 0;

    for (
        let value = 0;
        value < 256;
        value++
    ) {

        backgroundWeight +=
            histogram[value];

        if (backgroundWeight === 0) {
            continue;
        }

        const foregroundWeight =
            total
            - backgroundWeight;

        if (foregroundWeight === 0) {
            break;
        }

        backgroundSum +=
            value
            * histogram[value];

        const backgroundMean =
            backgroundSum
            / backgroundWeight;

        const foregroundMean =
            (
                weightedTotal
                - backgroundSum
            )
            / foregroundWeight;

        const difference =
            backgroundMean
            - foregroundMean;

        const variance =
            backgroundWeight
            * foregroundWeight
            * difference
            * difference;

        if (
            variance
            > maximumVariance
        ) {

            maximumVariance =
                variance;

            threshold =
                value;

        }

    }

    return threshold;

}


function semana10MaskToDataUrl(
    gray,
    width,
    height,
    threshold
) {

    const canvas =
        createSemana10Canvas(
            width,
            height
        );

    const context =
        canvas.getContext(
            "2d"
        );

    const output =
        context.createImageData(
            width,
            height
        );

    for (
        let pixel = 0;
        pixel < gray.length;
        pixel++
    ) {

        const offset =
            pixel * 4;

        const value =
            gray[pixel]
            > threshold
                ? 255
                : 0;

        output.data[offset] = value;
        output.data[offset + 1] = value;
        output.data[offset + 2] = value;
        output.data[offset + 3] = 255;

    }

    context.putImageData(
        output,
        0,
        0
    );

    return canvas.toDataURL(
        "image/png"
    );

}


function sampleSemana10Gray(
    gray,
    width,
    height,
    x,
    y
) {

    const x0 =
        Math.floor(x);

    const y0 =
        Math.floor(y);

    const x1 =
        Math.min(
            x0 + 1,
            width - 1
        );

    const y1 =
        Math.min(
            y0 + 1,
            height - 1
        );

    const dx = x - x0;
    const dy = y - y0;

    const top =
        gray[y0 * width + x0]
        * (1 - dx)
        + gray[y0 * width + x1]
        * dx;

    const bottom =
        gray[y1 * width + x0]
        * (1 - dx)
        + gray[y1 * width + x1]
        * dx;

    return (
        top * (1 - dy)
        + bottom * dy
    );

}


function semana10LbpToDataUrl(
    gray,
    width,
    height
) {

    const points = 16;
    const radius = 2;

    const canvas =
        createSemana10Canvas(
            width,
            height
        );

    const context =
        canvas.getContext(
            "2d"
        );

    const output =
        context.createImageData(
            width,
            height
        );

    for (
        let y = 0;
        y < height;
        y++
    ) {

        for (
            let x = 0;
            x < width;
            x++
        ) {

            const pixel =
                y * width + x;

            let lbpValue = 0;

            if (
                x >= radius
                && x < width - radius
                && y >= radius
                && y < height - radius
            ) {

                const center =
                    gray[pixel];

                const bits =
                    new Uint8Array(
                        points
                    );

                let ones = 0;

                for (
                    let point = 0;
                    point < points;
                    point++
                ) {

                    const angle =
                        2
                        * Math.PI
                        * point
                        / points;

                    const sampleX =
                        x
                        + radius
                        * Math.cos(angle);

                    const sampleY =
                        y
                        - radius
                        * Math.sin(angle);

                    const neighbor =
                        sampleSemana10Gray(
                            gray,
                            width,
                            height,
                            sampleX,
                            sampleY
                        );

                    bits[point] =
                        neighbor >= center
                            ? 1
                            : 0;

                    ones +=
                        bits[point];

                }

                let transitions = 0;

                for (
                    let point = 0;
                    point < points;
                    point++
                ) {

                    const next =
                        (point + 1)
                        % points;

                    if (
                        bits[point]
                        !== bits[next]
                    ) {

                        transitions++;

                    }

                }

                const uniformValue =
                    transitions <= 2
                        ? ones
                        : points + 1;

                lbpValue =
                    Math.round(
                        uniformValue
                        / (points + 1)
                        * 255
                    );

            }

            const offset =
                pixel * 4;

            output.data[offset] =
                lbpValue;

            output.data[offset + 1] =
                lbpValue;

            output.data[offset + 2] =
                lbpValue;

            output.data[offset + 3] =
                255;

        }

    }

    context.putImageData(
        output,
        0,
        0
    );

    return canvas.toDataURL(
        "image/png"
    );

}


async function buildSemana10LocalVisuals(file) {

    const image =
        await loadSemana10ImageSource(
            file
        );

    const sourceWidth =
        image.width;

    const sourceHeight =
        image.height;

    const maximumSide =
        900;

    const scale =
        Math.min(
            1,
            maximumSide
            / Math.max(
                sourceWidth,
                sourceHeight
            )
        );

    const width =
        Math.max(
            1,
            Math.round(
                sourceWidth
                * scale
            )
        );

    const height =
        Math.max(
            1,
            Math.round(
                sourceHeight
                * scale
            )
        );

    const canvas =
        createSemana10Canvas(
            width,
            height
        );

    const context =
        canvas.getContext(
            "2d",
            {
                willReadFrequently:
                    true
            }
        );

    context.drawImage(
        image,
        0,
        0,
        width,
        height
    );

    if (
        typeof image.close
        === "function"
    ) {

        image.close();

    }

    const imageData =
        context.getImageData(
            0,
            0,
            width,
            height
        );

    const gray =
        createSemana10GrayValues(
            imageData
        );

    const localOtsu =
        calculateSemana10OtsuThreshold(
            gray
        );

    return {
        gris:
            semana10GrayToDataUrl(
                gray,
                width,
                height
            ),

        otsu:
            semana10MaskToDataUrl(
                gray,
                width,
                height,
                localOtsu
            ),

        lbp:
            semana10LbpToDataUrl(
                gray,
                width,
                height
            ),

        source: {
            gray,
            width,
            height,
            localOtsu
        }
    };

}


function updateSemana10OtsuPreviewFromBackend(
    normalizedThreshold
) {

    if (!semana10LocalVisualData) {
        return;
    }

    const threshold =
        Number(
            normalizedThreshold
        );

    if (
        !Number.isFinite(
            threshold
        )
    ) {

        return;
    }

    const threshold255 =
        Math.max(
            0,
            Math.min(
                255,
                threshold * 255
            )
        );

    semana10Visuals.otsu =
        semana10MaskToDataUrl(
            semana10LocalVisualData.gray,
            semana10LocalVisualData.width,
            semana10LocalVisualData.height,
            threshold255
        );

}


// ============================================================
// MOSTRAR ERROR
// ============================================================

function showSemana10Error(
    message
) {

    setText(
        "semana10ErrorText",
        message
    );


    setHidden(
        "semana10Loading",
        true
    );

    setHidden(
        "semana10Results",
        true
    );

    setHidden(
        "semana10Error",
        false
    );

}


// ============================================================
// ESTADO DEL BOTÓN
// ============================================================

function setSemana10Loading(
    loading
) {

    const button =
        document.getElementById(
            "semana10AnalyzeButton"
        );

    const textElement =
        document.getElementById(
            "semana10AnalyzeText"
        );


    if (!button) {
        return;
    }


    button.disabled =
        loading;


    button.classList.toggle(
        "is-loading",
        loading
    );


    if (textElement) {

        textElement.textContent =
            loading
                ? "Analizando fotografía..."
                : "Analizar estado físico";

    }


    setHidden(
        "semana10Loading",
        !loading
    );

}


// ============================================================
// EJECUTAR ANÁLISIS
// ============================================================

async function runSemana10() {

    if (!semana10SelectedFile) {

        showSemana10Error(
            "Selecciona una fotografía antes de analizar."
        );

        return;
    }


    setSemana10Loading(
        true
    );


    setHidden(
        "semana10Error",
        true
    );

    setHidden(
        "semana10Results",
        true
    );


    try {

        const formData =
            new FormData();


        formData.append(
            "imagen",
            semana10SelectedFile
        );


        const response =
            await fetch(
                "/api/semana10",
                {
                    method:
                        "POST",

                    body:
                        formData
                }
            );


        let data = null;


        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "El backend devolvió una respuesta no válida."
            );

        }


        if (
            !response.ok
            || !data.success
        ) {

            throw new Error(
                data.error
                || "No fue posible analizar la fotografía."
            );

        }


        renderSemana10Result(
            data
        );


    } catch (error) {

        showSemana10Error(
            error.message
        );


    } finally {

        setSemana10Loading(
            false
        );

    }

}


// ============================================================
// SIMILITUD RELATIVA
// ============================================================

function calculateSemana10Similarity(
    cleanDistance,
    dirtyDistance
) {

    const clean =
        Number.isFinite(
            cleanDistance
        )
            ? Math.max(
                cleanDistance,
                0
            )
            : 0;


    const dirty =
        Number.isFinite(
            dirtyDistance
        )
            ? Math.max(
                dirtyDistance,
                0
            )
            : 0;


    const cleanCloseness =
        1 / (
            1 + clean
        );


    const dirtyCloseness =
        1 / (
            1 + dirty
        );


    const total =
        cleanCloseness
        + dirtyCloseness;


    if (total <= 0) {

        return {
            clean: 50,
            dirty: 50
        };

    }


    return {
        clean:
            cleanCloseness
            / total
            * 100,

        dirty:
            dirtyCloseness
            / total
            * 100
    };

}


// ============================================================
// MOSTRAR RESULTADO
// ============================================================

function renderSemana10Result(
    data
) {

    const cleanDistance =
        Number(
            data.distancia_limpio
        );


    const dirtyDistance =
        Number(
            data.distancia_sucio
        );


    const state =
        data.estado
        || "";


    const similarity =
        calculateSemana10Similarity(
            cleanDistance,
            dirtyDistance
        );


    // --------------------------------------------------------
    // Artefactos visuales
    // --------------------------------------------------------

    const artifacts =
        data.artifacts
        || {};


    semana10Visuals = {
        original:
            semana10PreviewUrl,

        gris:
            normalizeSemana10ArtifactUrl(
                artifacts.gris
                || artifacts.gray
            )
            || semana10Visuals.gris,

        otsu:
            normalizeSemana10ArtifactUrl(
                artifacts.otsu
                || artifacts.mask
            )
            || semana10Visuals.otsu,

        lbp:
            normalizeSemana10ArtifactUrl(
                artifacts.lbp
            )
            || semana10Visuals.lbp
    };


    if (
        !artifacts.otsu
        && !artifacts.mask
    ) {

        updateSemana10OtsuPreviewFromBackend(
            data.umbral_otsu
        );

    }


    const hero =
        document.getElementById(
            "semana10Hero"
        );

    const badge =
        document.getElementById(
            "semana10StatusBadge"
        );

    const statusIcon =
        document.getElementById(
            "semana10StatusIcon"
        );

    const recommendation =
        document.getElementById(
            "semana10RecommendationCard"
        );


    [
        hero,
        badge,
        recommendation
    ].forEach(
        element => {

            element?.classList.remove(
                "clean",
                "dirty"
            );

        }
    );


    const isDirty =
        state
        ===
        "SIMILAR_A_REFERENCIA_SUCIA";


    if (isDirty) {

        hero?.classList.add(
            "dirty"
        );

        badge?.classList.add(
            "dirty"
        );

        recommendation?.classList.add(
            "dirty"
        );


        setText(
            "semana10StatusIcon",
            "!"
        );

        setText(
            "semana10Estado",
            "Posible acumulación de suciedad"
        );

        setText(
            "semana10EstadoDescripcion",
            "La fotografía presenta características visuales más cercanas a la referencia con acumulación de suciedad."
        );

        setText(
            "semana10StatusBadge",
            "REVISIÓN RECOMENDADA"
        );

    } else {

        hero?.classList.add(
            "clean"
        );

        badge?.classList.add(
            "clean"
        );

        recommendation?.classList.add(
            "clean"
        );


        setText(
            "semana10StatusIcon",
            "✓"
        );

        setText(
            "semana10Estado",
            "Condición visual favorable"
        );

        setText(
            "semana10EstadoDescripcion",
            "La fotografía presenta características visuales más cercanas a la referencia del sistema de ventilación limpio."
        );

        setText(
            "semana10StatusBadge",
            "ESTADO FAVORABLE"
        );

    }


    // --------------------------------------------------------
    // Barras de similitud
    // --------------------------------------------------------

    setText(
        "semana10SimilarityClean",
        `${similarity.clean.toFixed(1)}%`
    );

    setText(
        "semana10SimilarityDirty",
        `${similarity.dirty.toFixed(1)}%`
    );


    const cleanBar =
        document.getElementById(
            "semana10BarClean"
        );

    const dirtyBar =
        document.getElementById(
            "semana10BarDirty"
        );


    if (cleanBar) {

        cleanBar.style.width =
            "0%";

        cleanBar.parentElement?.setAttribute(
            "aria-valuenow",
            similarity.clean.toFixed(1)
        );

    }


    if (dirtyBar) {

        dirtyBar.style.width =
            "0%";

        dirtyBar.parentElement?.setAttribute(
            "aria-valuenow",
            similarity.dirty.toFixed(1)
        );

    }


    requestAnimationFrame(
        () => {

            if (cleanBar) {

                cleanBar.style.width =
                    `${similarity.clean}%`;

            }


            if (dirtyBar) {

                dirtyBar.style.width =
                    `${similarity.dirty}%`;

            }

        }
    );


    // --------------------------------------------------------
    // Distancias
    // --------------------------------------------------------

    setText(
        "semana10DistanciaLimpio",
        Number.isFinite(
            cleanDistance
        )
            ? cleanDistance.toFixed(4)
            : "-"
    );

    setText(
        "semana10DistanciaSucio",
        Number.isFinite(
            dirtyDistance
        )
            ? dirtyDistance.toFixed(4)
            : "-"
    );


    const winner =
        document.getElementById(
            "semana10SimilarityWinner"
        );


    if (winner) {

        const dirtyWins =
            Number.isFinite(
                dirtyDistance
            )
            && Number.isFinite(
                cleanDistance
            )
            && dirtyDistance
            < cleanDistance;


        winner.textContent =
            dirtyWins
                ? "Mayor similitud visual: referencia con suciedad"
                : "Mayor similitud visual: referencia limpia";


        winner.className =
            dirtyWins
                ? "semana10-similarity-summary dirty"
                : "semana10-similarity-summary clean";

    }


    // --------------------------------------------------------
    // Métricas
    // --------------------------------------------------------

    setText(
        "semana10Otsu",
        formatSemana10Number(
            data.umbral_otsu,
            4
        )
    );

    setText(
        "semana10Regiones",
        data.regiones
        ?? "-"
    );

    setText(
        "semana10Area",
        formatSemana10Number(
            data.area_promedio,
            2
        )
    );

    setText(
        "semana10Desviacion",
        formatSemana10Number(
            data.desviacion_area,
            2
        )
    );


    setText(
        "semana10Recomendacion",
        data.recomendacion
        || "-"
    );


    setHidden(
        "semana10Error",
        true
    );

    setHidden(
        "semana10Results",
        false
    );


    const preferredVisual =
        semana10Visuals.gris
            ? "gris"
            : "original";


    showSemana10Process(
        preferredVisual
    );


    document.getElementById(
        "semana10Results"
    )?.scrollIntoView({
        behavior:
            "smooth",

        block:
            "start"
    });

}


// ============================================================
// FORMATEAR DATOS DE SEMANA 10
// ============================================================

function formatSemana10Number(
    value,
    decimals
) {

    const number =
        Number(
            value
        );


    if (!Number.isFinite(number)) {
        return "-";
    }


    return number.toFixed(
        decimals
    );

}


// ============================================================
// UTILIDAD DE VISIBILIDAD
// ============================================================

function setHidden(
    id,
    hidden
) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.hidden =
            hidden;

    }

}
