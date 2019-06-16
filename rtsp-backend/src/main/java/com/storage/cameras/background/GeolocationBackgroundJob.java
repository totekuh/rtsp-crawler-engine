package com.storage.cameras.background;

import com.storage.cameras.dao.CameraDao;
import com.storage.cameras.model.Camera;
import lombok.AllArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@AllArgsConstructor
public class GeolocationBackgroundJob {

    private final CameraDao cameraDao;

    @Scheduled
    public void lookup() {
        final List<Camera> cameras = cameraDao.getAll();

    }
}
