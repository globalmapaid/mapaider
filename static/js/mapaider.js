const createTitlePanel = (mapTitle) => {
    var title = new L.Control()

    title.onAdd = function (map) {
        this._div = L.DomUtil.create("div", "info")
        this.update()
        return this._div
    }
    title.update = function () {
        this._div.innerHTML = "<h2>" + mapTitle + "</h2>"
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

const createLayerPanel = (mapLayers, layerStyle, collapsed = true) => {
    let baseMaps = {}

    let layerSet = {}
    mapLayers.forEach((item) => {
        const style = layerStyle(item.uuid)
        const icon = style.icon.options.iconUrl
        const label = '<img alt="' + item.name + '" src="' + icon + '" style="height:16px; width:16px"> ' + item.name
        layerSet[label] = layers[item.uuid]
    })

    layerSet = {
        ...layerSet,
        "Background map": layer_Backgroundmap_2,
        "Satellite background": layer_Satellitebackground_0,
    }
    /*
        L.control
            .layers(baseMaps, {
                /*
                '<img src="/static/legend/GardenPledges_11.png" /> Garden Pledges':
                    layers["garden-pledges"],
                '<img src="/static/legend/GovernmentPledges_10.png" /> Government Pledges':
                    layers["government-pledges"],
                '<img src="/static/legend/FarmPledges_8.png" /> Farm Pledges':
                    layers["farm-pledges"],
                '<img src="/static/legend/ChurchPledge_6.png" /> Church Pledge':
                    layers["church-pledges"],
                '<img src="/static/legend/SchoolPledges_4.png" /> School Pledges':
                    layers["school-pledges"],
                '<img src="/static/legend/RailwayStationPledges.png" /> Railway Station Pledges':
                    layers["railway-station-pledges"],


                "Background map": layer_Backgroundmap_2,
                "Satellite background": layer_Satellitebackground_0,
            }, {collapsed: collapsed})
            .addTo(map)*/

    L.control.layers(baseMaps, layerSet, {collapsed: collapsed}).addTo(map)

}

var layers = {}
