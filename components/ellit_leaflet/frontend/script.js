const { Streamlit, withStreamlitConnection } = window.streamlitComponentLib;

class EllitLeaflet extends React.Component {
  constructor(props) {
    super(props);
    this.map = null;
    this.mapRef = React.createRef();
  }

  componentDidMount() {
    this.renderMap();
  }

  componentDidUpdate() {
    this.renderMap();
  }

  renderMap() {
    const args = this.props.args || {};
    const raw = args.threatData;

    if (!raw) {
      return;
    }

    let threatData;
    try {
      threatData = JSON.parse(raw);
    } catch (e) {
      console.error("Error parsing threatData JSON:", e);
      return;
    }

    const height = args.height || 520;

    // Si ya hay mapa, lo destruimos
    if (this.map !== null) {
      this.map.remove();
      this.map = null;
    }

    // Crear mapa
    this.map = L.map(this.mapRef.current, {
      zoomControl: true,
      scrollWheelZoom: true,
    }).setView([20, 0], 2);

    // Tile base
    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
      {
        maxZoom: 19,
      }
    ).addTo(this.map);

    // Dibujar países
    (threatData.countries || []).forEach((country) => {
      const riskColor =
        country.risk >= 80 ? "#FF0080" : country.risk >= 60 ? "#FF5FB0" : "#00B4FF";

      const marker = L.circleMarker([country.lat, country.lon], {
        radius: 15,
        color: riskColor,
        fillColor: riskColor,
        fillOpacity: 0.7,
        className: "ellit-risk-circle",
      }).addTo(this.map);

      marker.bindPopup(
        `<b>${country.country}</b><br>
         Riesgo: ${country.risk}%<br>
         CVEs activas: ${country.cves}`
      );

      marker.on("click", () => {
        Streamlit.setComponentValue({
          event: "country_clicked",
          country: country.country,
          risk: country.risk,
          cves: country.cves,
        });
      });
    });

    // Ajustar alto del iframe
    Streamlit.setFrameHeight(height);
  }

  render() {
    const height = (this.props.args && this.props.args.height) || 520;
    const style = {
      width: "100%",
      height: `${height}px`,
    };
    return React.createElement("div", { ref: this.mapRef, style });
  }
}

const WrappedComponent = withStreamlitConnection(EllitLeaflet);
ReactDOM.render(
  React.createElement(WrappedComponent),
  document.getElementById("root")
);

