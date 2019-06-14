package com.storage.cameras.rest;

import com.storage.cameras.service.CameraService;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import static com.storage.cameras.model.RequestPath.CAMERAS_URL;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.springframework.http.ResponseEntity.badRequest;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequestMapping(CAMERAS_URL)
@AllArgsConstructor
public class CameraRestController {

    private final CameraService cameraService;

    @PostMapping("/import")
    public ResponseEntity receive(@RequestBody final PostCameraParams params) {
        return ok(cameraService.save(params));
    }

    @SneakyThrows
    @GetMapping
    public ResponseEntity get(@RequestParam(required = false) final Long id,
                              @RequestParam(required = false) final String rtspUrl) {
        if (id != null) {
            return ok(cameraService.get(id));
        }
        if (isNotBlank(rtspUrl)) {
            return ok(cameraService.get(rtspUrl));
        }
        return badRequest().build();
    }

}
