const createTitlePanel = (mapTitle) => {
    var title = new L.Control({position: 'bottomleft'})

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
    if (links.length > 0) {
        var linksPanel = new L.Control({position: 'bottomright'})

        linksPanel.onAdd = function (map) {
            this._div = L.DomUtil.create("div", "bg-white p-2 rounded-md")
            this.update()
            return this._div
        }
        linksPanel.update = function () {
            let panelContent = '<strong>How about</strong>'
            links.forEach((item) => {
                panelContent += `
<div>
<a href='${item.url}' target='_blank' class="hover:text-orange-500">
${item.label}
</a>
</div>`
            })
            this._div.innerHTML = panelContent
        }
        linksPanel.addTo(map)
    }
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

const createLayerPanel = (baseMaps, mapLayers, layerStyle, collapsed = true) => {
    let overlayMaps = {}

    mapLayers.forEach((mapLayer) => {
        const style = layerStyle(mapLayer.uuid)
        const icon = style.icon.options.iconUrl

        let layerLabel = mapLayer.layer.name
        const label = '<img alt="' + layerLabel + '" src="' + icon + '" class="inline" style="height:16px; width:16px"> ' + layerLabel
        overlayMaps[label] = layers[mapLayer.uuid]
    })

    overlayMaps = {
        ...overlayMaps,
        //'Street Map': layer_StreetMap,
        //'Satellite Map': layer_SatelliteMap,
    }

    L.control.layers(baseMaps, overlayMaps, {collapsed: collapsed}).addTo(map)

}

var layers = {}
