package com.storage.cameras.model;

public enum CameraStatus {
    /**
     * Clearly open access. Just connect to it.
     */
    OPEN,

    /**
     * RTSP stream is exists, but there are no valid credentials.
     */
    UNAUTHORIZED,

    /**
     * RTSP stream is exists, but an actual url was not found.
     */
    NOT_FOUND,

    /**
     * RTSP connection cannot be established or stream does not exist.
     * Cameras with this status should not present for a long time in the database and must be deleted at some point.
     */
    CONNECTION_REFUSED;
}
