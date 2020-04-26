package com.storage.cameras.background;

import com.storage.cameras.model.Camera;
import com.storage.cameras.service.CameraService;
import com.storage.cameras.service.LabelService;
import java.util.List;
import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Slf4j
public class DeleteUnconnectedCamerasBackgroundJob {
    private final CameraService cameraService;
    private final LabelService labelService;

    @PostConstruct
    public void lookup() {
        final DeleteUnconnectedCamerasThread thread = new DeleteUnconnectedCamerasThread(cameraService,
                labelService);
        new Thread(thread).start();
    }

    @AllArgsConstructor
    private static final class DeleteUnconnectedCamerasThread implements Runnable {
        private final CameraService cameraService;
        private final LabelService labelService;
        private static final long SLEEPING_TIMER_IN_MS = 3600 * 1000;

        @Override
        public void run() {
            while (true) {
                final List<Camera> camerasToDelete = cameraService.getAllUnconnected();
                if (isNotEmpty(camerasToDelete)) {
                    log.info("Starting a deletion job of unconnected cameras. " +
                            "Number of cameras to delete: {}", camerasToDelete.size());

                    camerasToDelete.forEach(camera -> {
                        labelService.unlinkLabelsFromCamera(camera.getId());
                        cameraService.delete(camera.getId());
                    });
                    log.info("Deletion job has finished successfully.");
                } else {
                    log.info("No unconnected cameras have been received for the deletion job");
                }
                log.info("Sleeping for the {} minutes", (SLEEPING_TIMER_IN_MS / 1000) / 60);
                try {
                    Thread.sleep(SLEEPING_TIMER_IN_MS);
                    log.info("Awaking from sleep, getting new unconnected cameras");
                } catch (final InterruptedException e) {
                    log.error("Deletion thread was interrupted.", e);
                    throw new IllegalStateException(e);
                }
            }
        }
    }

}
