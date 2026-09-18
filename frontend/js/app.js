// ============================================================
// ELEMENTOS PRINCIPALES
// ============================================================

const menuItems = document.querySelectorAll(
    ".menu-item"
);

const sections = document.querySelectorAll(
    ".content-section"
);

const pageTitle = document.getElementById(
    "page-title"
);


// ============================================================
// TÍTULOS DE LAS SECCIONES
// ============================================================

const titles = {

    inicio:
        "Panel del proyecto",

    semana2:
        "Semana 2 · Fundamentos",

    semana3:
        "Semana 3 · Taxonomía",

    semana4:
        "Semana 4 · Búsqueda y decisión",

    semana5:
        "Semana 5 · Sistema híbrido",

    semana7:
        "Semana 7 · Representaciones del reconocimiento",

    arquitectura:
        "Arquitectura del proyecto",
};


// ============================================================
// NAVEGACIÓN
// ============================================================

function showSection(
    sectionId
) {

    sections.forEach(
        section => {

            section.classList.remove(
                "active"
            );

        }
    );


    menuItems.forEach(
        item => {

            item.classList.remove(
                "active"
            );

        }
    );


    const section =
        document.getElementById(
            sectionId
        );


    if (section) {

        section.classList.add(
            "active"
        );

    }


    const menu =
        document.querySelector(
            `[data-section="${sectionId}"]`
        );


    if (menu) {

        menu.classList.add(
            "active"
        );

    }


    if (pageTitle) {

        pageTitle.textContent =
            titles[sectionId]
            || "Proyecto IA";

    }


    window.location.hash =
        sectionId;


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


// ============================================================
// MENÚ
// ============================================================

menuItems.forEach(
    item => {

        item.addEventListener(
            "click",
            () => {

                showSection(
                    item.dataset.section
                );

            }
        );

    }
);


// ============================================================
// ABRIR SEMANA
// ============================================================

function openWeek(
    sectionId
) {

    showSection(
        sectionId
    );

}


// ============================================================
// VISUALIZAR ARCHIVOS
// ============================================================

async function loadFile(
    path,
    targetId
) {

    const target =
        document.getElementById(
            targetId
        );


    if (!target) {
        return;
    }


    target.textContent =
        "Cargando archivo...";


    try {

        // Elimina ../ si todavía existe
        // en alguna ruta del HTML.
        const cleanPath =
            path.replace(
                /^(\.\.\/)+/,
                ""
            );


        const response =
            await fetch(
                `/project/${cleanPath}`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );

        }


        const text =
            await response.text();


        target.textContent =
            text;


    } catch (error) {

        target.textContent =
            "No fue posible cargar el archivo.\n\n"
            + `Error: ${error.message}`;

    }

}


// ============================================================
// EJECUTAR CÓDIGO PYTHON
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


    output.classList.remove(
        "success",
        "error"
    );


    output.textContent =
        "$ Ejecutando...\n\n"
        + "Por favor espera.";


    try {

        const response =
            await fetch(
                `/api/run/${scriptName}`,
                {
                    method: "POST"
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error
                || "Error de ejecución."
            );

        }


        let terminalText = "";

        terminalText +=
            `$ python3 ${result.script}\n`;

        terminalText +=
            "========================================\n\n";


        if (result.stdout) {

            terminalText +=
                result.stdout;

        }


        if (result.stderr) {

            terminalText +=
                "\n\n--- STDERR ---\n";

            terminalText +=
                result.stderr;

        }


        terminalText +=
            "\n\n========================================\n";

        terminalText +=
            `Código de salida: ${result.returncode}`;


        if (result.success) {

            terminalText +=
                "\nEstado: EJECUCIÓN CORRECTA";

            output.classList.add(
                "success"
            );

        } else {

            terminalText +=
                "\nEstado: ERROR";

            output.classList.add(
                "error"
            );

        }


        output.textContent =
            terminalText;


    } catch (error) {

        output.classList.add(
            "error"
        );


        output.textContent =
            "$ Error al ejecutar\n\n"
            + error.message;

    }

}


// ============================================================
// COMPROBAR BACKEND
// ============================================================

async function checkBackend() {

    try {

        const response =
            await fetch(
                "/api/status"
            );


        const data =
            await response.json();


        console.log(
            "Backend:",
            data
        );


    } catch (error) {

        console.error(
            "Flask no está disponible.",
            error
        );

    }

}


// ============================================================
// RECUPERAR SECCIÓN DESDE LA URL
// ============================================================

const hash =
    window.location.hash.replace(
        "#",
        ""
    );


if (
    hash
    && document.getElementById(hash)
) {

    showSection(
        hash
    );

}


// ============================================================
// INICIO
// ============================================================

checkBackend();
// ============================================================
// SEMANA 7
// ============================================================

async function runSemana7() {

    const output =
        document.getElementById(
            "output-semana7"
        );


    const temperature =
        document.getElementById(
            "s7-temperatura"
        ).value;


    const load =
        document.getElementById(
            "s7-carga"
        ).value;


    const errors =
        document.getElementById(
            "s7-errores"
        ).value;


    const sequence =
        document.getElementById(
            "s7-secuencia"
        ).value
            .trim()
            .toUpperCase();


    output.classList.remove(
        "success",
        "error"
    );


    output.textContent =
        "$ Analizando servidor...\n";


    try {

        const response =
            await fetch(
                "/api/semana7",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            temperatura:
                                temperature,

                            carga:
                                load,

                            errores:
                                errors,

                            secuencia:
                                sequence,
                        }
                    )
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error
                || "Error en Semana 7."
            );

        }


        let text = "";

        text +=
            "$ python semana07_representaciones.py\n";

        text +=
            "========================================\n\n";


        if (result.stdout) {

            text +=
                result.stdout;

        }


        if (result.stderr) {

            text +=
                "\n\n--- STDERR ---\n";

            text +=
                result.stderr;

        }


        text +=
            "\n\n========================================\n";


        if (result.success) {

            text +=
                "Estado: EJECUCIÓN CORRECTA";

            output.classList.add(
                "success"
            );

        } else {

            text +=
                "Estado: ERROR";

            output.classList.add(
                "error"
            );

        }


        output.textContent =
            text;


    } catch (error) {

        output.classList.add(
            "error"
        );


        output.textContent =
            "$ Error\n\n"
            + error.message;

    }

}