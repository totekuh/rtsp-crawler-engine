package com.storage.cameras.model;

public enum CameraStatus {
    /**
     * Clearly open access. Just connect to it.
     */
    OPEN,

    /**
     * RTSP stream is exist, but there are no valid credentials.
     */
    UNAUTHORIZED,

    /**
     * RTSP stream is exist, but an actual url was not found.
     */
    NOT_FOUND,

    /**
     * RTSP connection cannot be established or stream does not exist.
     * Cameras with this status should not present for a long time in the database and must be deleted at some point.
     */
    UNCONNECTED;
}
