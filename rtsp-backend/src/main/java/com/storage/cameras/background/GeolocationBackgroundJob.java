package com.storage.cameras.background;

import com.storage.cameras.model.Camera;
import com.storage.cameras.service.CameraService;
import java.util.List;
import java.util.Optional;
import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;
import static com.storage.cameras.util.XmlUtil.extractTag;
import static java.lang.String.format;
import static java.util.Optional.empty;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import static org.apache.commons.lang3.StringUtils.isBlank;

@Component
@AllArgsConstructor
@Slf4j
public class GeolocationBackgroundJob {
    private final CameraService cameraService;

    @PostConstruct
    public void lookup() {
        final GeolocationThread thread = new GeolocationThread(cameraService);
        new Thread(thread).start();
    }

    @AllArgsConstructor
    private static final class GeolocationThread implements Runnable {
        private final CameraService cameraService;
        private static final long SLEEPING_TIMER_IN_MS = 3600 * 1000;

        @Override
        public void run() {
            while (true) {
                final List<Camera> camerasToLookup = cameraService.getWithNoGeolocation();
                if (isNotEmpty(camerasToLookup)) {
                    log.info("Starting a new geolocation job. Number of cameras to lookup: {}", camerasToLookup.size());
                    camerasToLookup
                            .forEach(camera -> doGeolocationLookup(camera.getIpAddress())
                                    .ifPresent(geolocationResult -> {
                                        camera.setCity(geolocationResult.getCity());
                                        camera.setCountryName(geolocationResult.getCountryName());
                                        camera.setCountryCode(geolocationResult.getCountryCode());
                                        camera.setIsp(geolocationResult.getIsp());
                                    }));
                    cameraService.save(camerasToLookup);
                    log.info("Geolocation job has finished successfully.");
                } else {
                    log.info("No cameras have been received for the geolocation lookup");
                }
                log.info("Sleeping for the {} minutes", (SLEEPING_TIMER_IN_MS / 1000) / 60);
                try {
                    Thread.sleep(SLEEPING_TIMER_IN_MS);
                    log.info("Awaking from sleep, getting new cameras");
                } catch (final InterruptedException e) {
                    log.error("Geolocation thread was interrupted.", e);
                    throw new IllegalStateException(e);
                }
            }
        }

        private Optional<GeolocationResult> doGeolocationLookup(final String ipAddress) {
            final String url = format("http://api.geoiplookup.net/?query=%s", ipAddress);
            try {
                final String responseBody = new RestTemplate().getForObject(url, String.class);
                if (isBlank(responseBody)) {
                    log.warn("[{}] Geolocation API responded with an empty message body.", ipAddress);
                    return empty();
                }
                if (responseBody.contains("<result>") && responseBody.contains(ipAddress)) {
                    final GeolocationResult result = new GeolocationResult(
                            ipAddress,
                            extractTag(responseBody, "city"),
                            extractTag(responseBody, "countrycode"),
                            extractTag(responseBody, "countryname"),
                            extractTag(responseBody, "isp"));
                    log.info("[{}] Geolocation received: {}/{}/{}",
                            ipAddress,
                            result.getCity(),
                            result.getCountryName(),
                            result.getCountryCode());
                    return Optional.of(result);
                } else {
                    return empty();
                }
            } catch (final HttpClientErrorException | HttpServerErrorException e) {
                log.warn("[{}] Geolocation API responded with an error: {}/{}",
                        ipAddress,
                        e.getStatusCode(),
                        e.getResponseBodyAsString());
                return empty();
            } catch (final Exception ex) {
                log.error("[{}] Unexpected error during geolocation lookup", ipAddress, ex);
                return empty();
            }
        }

        @Data
        private static final class GeolocationResult {
            private final String ip;
            private final String city;
            private final String countryCode;
            private final String countryName;
            private final String isp;
        }
    }

}
