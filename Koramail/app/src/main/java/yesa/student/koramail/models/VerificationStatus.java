package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

public class VerificationStatus {
    @SerializedName("verified")
    private Boolean verified;

    public Boolean getVerified() {
        return verified;
    }

    public void setVerified(Boolean verified) {
        this.verified = verified;
    }
}
