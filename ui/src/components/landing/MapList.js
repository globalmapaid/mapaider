import React from "react";
import {Card, CardContent} from "@mui/material";

const MapList = (props) => {
    let maps = props.maps ?? null

    if (maps != null) {
        return (
            <React.Fragment>
                {
                    maps.map((mapItem) => {
                        return (
                            <Card key={mapItem.uuid}>
                                <CardContent>
                                    <a href={"/mapaider/map/" + mapItem.slug}>
                                        {mapItem.name}
                                    </a>
                                </CardContent>
                            </Card>
                        )
                    })
                }
            </React.Fragment>
        )
    } else {
        return (<React.Fragment>Loading</React.Fragment>)
    }
}

export default MapList
