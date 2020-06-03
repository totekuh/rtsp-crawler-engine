package com.storage.cameras.background;

import static com.storage.cameras.model.CameraStatus.OPEN;
import static java.lang.Thread.sleep;
import static java.util.stream.Collectors.toList;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import com.storage.cameras.model.Camera;
import com.storage.cameras.service.CameraService;
import com.storage.cameras.service.LabelService;
import java.util.List;
import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Slf4j
public class CheckCamerasConnectivityBackgroundJob {
    private final CameraService cameraService;
    private final LabelService labelService;

    @PostConstruct
    public void lookup() {
        final CheckCamerasConnectivityThread thread = new CheckCamerasConnectivityThread(cameraService, labelService);
        new Thread(thread).start();
    }

    @AllArgsConstructor
    private static final class CheckCamerasConnectivityThread implements Runnable {
        private final CameraService cameraService;
        private final LabelService labelService;
        private static final long SLEEPING_TIMER_IN_MS = 1800 * 1000;

        @Override
        public void run() {
            while (true) {
                final List<Camera> cameras = cameraService.getAll()
                        .stream()
                        .filter(camera -> camera.getStatus() == OPEN)
                        .collect(toList());
                if (isNotEmpty(cameras)) {
                    log.info("Starting a new check-connectivity background job for {} cameras", cameras.size());
                    cameras.forEach(camera -> {
                        if (camera.isReachable()) {
                            // do nothing
                        } else {
                            log.warn("Lost connection to the {} camera in {}, deleting it from the database",
                                    camera.getUrl(),
                                    camera.getCountryName());
                            labelService.unlinkLabelsFromCamera(camera.getId());
                            cameraService.delete(camera.getId());
                        }
                    });
                } else {
                    log.info("No open cameras have been collected for the check-connectivity background job");
                }

                log.info("Sleeping for the {} minutes", (SLEEPING_TIMER_IN_MS / 1000) / 60);
                try {
                    sleep(SLEEPING_TIMER_IN_MS);
                    log.info("Awaking from sleep, getting new unconnected cameras");
                } catch (final InterruptedException e) {
                    log.error("Deletion thread was interrupted.", e);
                    throw new IllegalStateException(e);
                }
            }
        }
    }

}
