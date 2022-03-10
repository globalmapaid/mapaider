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

const createLinksPanel = () => {
    var links = new L.Control()

    links.onAdd = function (map) {
        this._div = L.DomUtil.create("div", "info")
        this.update()
        return this._div
    }
    links.update = function () {
        this._div.innerHTML = "<a href='https://www.globalmapaid.org/donate-now/'>Donate Map Aid</a>"
    }
    links.addTo(map)
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

    L.control.layers(baseMaps, layerSet, {collapsed: collapsed}).addTo(map)

}

var layers = {}
