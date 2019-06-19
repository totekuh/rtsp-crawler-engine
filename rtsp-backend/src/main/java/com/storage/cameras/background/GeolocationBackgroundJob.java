package com.storage.cameras.background;

import com.storage.cameras.dao.CameraDao;
import com.storage.cameras.model.Camera;
import java.util.List;
import lombok.AllArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class GeolocationBackgroundJob {

    private final CameraDao cameraDao;

    @Scheduled
    // adjust the annotation so this method will run each hour
    public void lookup() {
        final List<Camera> cameras = cameraDao.getAll();
        // get a geolocation result for each camera where city is null or countryName is null or countryCode is null
        // api.geoiplookup.net/?query=10.10.10.10
    }
}
