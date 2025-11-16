let map = null;

function loadMap(threatData, streamlitSendEvent) {
    if (map !== null) {
        map.remove();
    }

    map = L.map('map', {
        zoomControl: true,
        scrollWheelZoom: true
    }).setView([20, 0], 2);

    // Tile base estilizado (Carto)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19
    }).addTo(map);

    // Dibujar países con riesgo
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



function StreamlitComponent() {}

StreamlitComponent.prototype.onRender = function(event) {
    if (!event.detail.args.threatData) return;

    const threatData = JSON.parse(event.detail.args.threatData);

    loadMap(threatData, (payload) => {
        const event = new CustomEvent("streamlit:componentEvent", {
            detail: payload
        });
        window.parent.document.dispatchEvent(event);
    });
};

const component = new StreamlitComponent();

window.addEventListener("load", function() {
    window.parent.document.addEventListener("streamlit:render", component.onRender);
});
