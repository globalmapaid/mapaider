const filterGeoJSONbyType = (geojson, type) => {
    filteredFeatures = geojson.features.filter(
        (feature) => feature.properties.type == type
    )

    return {
        type: "FeatureCollection",
        features: filteredFeatures,
    }
}

const createTitlePanel = () => {
    var title = new L.Control()

    title.onAdd = function (map) {
        this._div = L.DomUtil.create("div", "info")
        this.update()
        return this._div
    }
    title.update = function () {
        this._div.innerHTML = "<h2>WildEast Map of Dreams</h2>"
    }
    title.addTo(map)
}

const createSearchPanel = () => {
    var osmGeocoder = new L.Control.Geocoder({
        collapsed: true,
        position: "topleft",
        text: "Search",
        title: "Testing",
    }).addTo(map)
    document.getElementsByClassName(
        "leaflet-control-geocoder-icon"
    )[0].className += " fa fa-search"
    document.getElementsByClassName("leaflet-control-geocoder-icon")[0].title +=
        "Search for a place"
}

const createLayerPanel = (collapsed=true) => {
    var baseMaps = {}
    L.control
        .layers(baseMaps, {
            '<img src="/static/legend/GardenPledges_11.png" /> Garden Pledges':
                layers["garden-pledges"],
            '<img src="/static/legend/GovernmentPledges_10.png" /> Government Pledges':
                layers["government-pledges"],
            '<img src="/static/legend/Government_9.png" /> Government':
            cluster_Government_9,
            '<img src="/static/legend/FarmPledges_8.png" /> Farm Pledges':
                layers["farm-pledges"],
            '<img src="/static/legend/Farms_7.png" /> Farms': cluster_Farms_7,
            '<img src="/static/legend/ChurchPledge_6.png" /> Church Pledge':
                layers["church-pledges"],
            '<img src="/static/legend/Churches_5.png" /> Churches':
            cluster_Churches_5,
            '<img src="/static/legend/SchoolPledges_4.png" /> School Pledges':
                layers["school-pledges"],
            '<img src="/static/legend/Schools_3.png" /> Schools': cluster_Schools_3,
            '<img src="/static/legend/RailwayStationPledges.png" /> Railway Station Pledges':
                layers["railway-station-pledges"],
            "Background map": layer_Backgroundmap_2,
            "WildEast background": layer_WildEastbackground_1,
            "Satellite background": layer_Satellitebackground_0,
        }, {collapsed: collapsed})
        .addTo(map)
}

const createEditPanel = () => {
    // Initialise the FeatureGroup to store editable layers
    map.addLayer(editableLayers)

    var drawPluginOptions = {
        position: "topright",
        draw: {
            polygon: {
                allowIntersection: false, // Restricts shapes to simple polygons
                drawError: {
                    color: "#e1e100", // Color the shape will turn when intersects
                    message: "<strong>Oh snap!<strong> you can't draw that!", // Message that will show when intersect
                },
                shapeOptions: {
                    color: "#97009c",
                },
            },
            // disable toolbar item by setting it to false
            polyline: false,
            circle: false, // Turns off this drawing tool
            circlemarker: false,
            rectangle: false,
            marker: true,
        },
        edit: {
            featureGroup: editableLayers,
            remove: true,
        },
    }

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    var drawControl = new L.Control.Draw(drawPluginOptions)
    map.addControl(drawControl)
}

var layers = {}
let editableLayers = new L.FeatureGroup()

function postGeoJSON(featureGroup) {
    let csrfToken = Cookies.get("csrftoken")

    const headers = {
        "X-CSRFToken": csrfToken,
    }

    let data = {
        type: document.querySelector('input[name="pledge-type"]:checked').value,
        first_name: document.getElementById("firstName").value,
        last_name: document.getElementById("lastName").value,
        email: document.getElementById("email").value,
        city: document.getElementById("city").value,
        phone: document.getElementById("phone").value,
        street: document.getElementById("street").value,
        postcode: document.getElementById("postcode").value,
        area: document.getElementById("area").value,
        measurement_unit: document.getElementById("measurementUnit").value,
        reason: document.getElementById("reason").value,
        geom: editableLayers.toGeoJSON().features[0].geometry,
    }

    axios
        .post(
            "/api/pledge/create",
            data,
            {headers: headers}
        )
        .then((response) => {
            // console.log(response.data)
        })
        .catch((error) => console.error(error))
}
