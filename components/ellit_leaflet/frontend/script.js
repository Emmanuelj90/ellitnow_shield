let map = null;

// ==========================
// Cargar y renderizar el mapa
// ==========================
function loadMap(threatData, streamlitSendEvent) {
    if (map !== null) {
        map.remove();
    }

    map = L.map('map', {
        zoomControl: true,
        scrollWheelZoom: true
    }).setView([20, 0], 2);

    // Capa base estilizada (Carto Dark)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19
    }).addTo(map);

    // ==========================
    // Dibujar países
    // ==========================
    threatData.countries.forEach(country => {
        const riskColor =
            country.risk >= 80 ? "#FF0080" :
            country.risk >= 60 ? "#FF5FB0" :
            "#00B4FF";

        const marker = L.circleMarker([country.lat, country.lng], {
            radius: 15,
            color: riskColor,
            fillColor: riskColor,
            fillOpacity: 0.7,
            className: "ellit-risk-circle"
        }).addTo(map);

        marker.bindPopup(`
            <b>${country.name}</b><br>
            Riesgo: ${country.risk}%<br>
            CVEs activas: ${country.cves}
        `);

        marker.on("click", () => {
            streamlitSendEvent({
                event: "country_clicked",
                country: country.name,
                risk: country.risk,
                cves: country.cves
            });
        });
    });
}



// =======================================
// Componente Streamlit (CORREGIDO)
// =======================================
function StreamlitComponent() {}

StreamlitComponent.prototype.onRender = function (event) {
    // Cambiado: ahora el backend envía `threatData`, NO `data`
    const raw = event.detail.args.threatData;
    if (!raw) return;

    const threatData = JSON.parse(raw);

    loadMap(threatData, (payload) => {
        const ev = new CustomEvent("streamlit:componentEvent", {
            detail: payload
        });
        window.parent.document.dispatchEvent(ev);
    });
};


// =======================================
// Inicialización requerida para Streamlit
// =======================================
window.initialize = () => {};

const component = new StreamlitComponent();

window.addEventListener("load", function () {
    window.parent.document.addEventListener(
        "streamlit:render",
        component.onRender.bind(component)
    );
});
