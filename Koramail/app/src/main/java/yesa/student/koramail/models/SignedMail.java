package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

public class SignedMail {
    @SerializedName("message")
    private String message;
    @SerializedName("signature")
    private String signature;

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getSignature() {
        return signature;
    }

    public void setSignature(String signature) {
        this.signature = signature;
    }
}
