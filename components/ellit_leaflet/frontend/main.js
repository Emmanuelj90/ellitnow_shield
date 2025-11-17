const root = document.getElementById("root");

// Esperar a que Streamlit envíe datos
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event) => {
  const data = event.detail.args.data;

  root.innerHTML = `
    <div id="map" style="width: 100%; height: 500px; border-radius: 12px;"></div>
  `;

  // Crear mapa Leaflet
  const map = L.map("map").setView([20, 0], 2.2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);

  // Dibujar puntos desde Streamlit
  if (data.countries) {
    data.countries.forEach((c) => {
      const marker = L.circleMarker([c.lat, c.lng], {
        color: "#ff0066",
        radius: 10,
        fillOpacity: 0.6,
      }).addTo(map);

      marker.bindPopup(`
        <b>${c.country}</b><br>
        Riesgo: ${c.risk}<br>
        CVEs: ${c.cves}<br>
      `);
    });
  }

  Streamlit.setFrameHeight(520);
});

Streamlit.setComponentReady();
Streamlit.callOnRender();
