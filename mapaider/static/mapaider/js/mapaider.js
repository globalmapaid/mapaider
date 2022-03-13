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

const createLinksPanel = (links = []) => {
    var linksPanel = new L.Control()

    linksPanel.onAdd = function (map) {
        this._div = L.DomUtil.create("div", "info")
        this.update()
        return this._div
    }
    linksPanel.update = function () {
        let panelContent = '<strong>Related Links</strong>'
        links.forEach((item) => {
            panelContent += `
<div>
<a href='${item.url}' target='_blank'>
${item.label}
</a>
</div>`
        })
        this._div.innerHTML = panelContent
    }
    linksPanel.addTo(map)
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
    let baseMaps = {
        'Street Map': layer_StreetMap,
        'Satellite': layer_SatelliteMap,
    }
    let overlayMaps = {}

    mapLayers.forEach((mapLayer) => {
        const style = layerStyle(mapLayer.uuid)
        const icon = style.icon.options.iconUrl

        let layerLabel = mapLayer.layer.name
        const label = '<img alt="' + layerLabel + '" src="' + icon + '" style="height:16px; width:16px"> ' + layerLabel
        overlayMaps[label] = layers[mapLayer.uuid]
    })

    L.control.layers(baseMaps, overlayMaps, {collapsed: collapsed}).addTo(map)

}

var layers = {}
