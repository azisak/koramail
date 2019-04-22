package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

public class EncryptedMail {
    @SerializedName("encrypted")
    private String encryptedMessage;

    public String getEncryptedMessage() {
        return encryptedMessage;
    }

    public void setEncryptedMessage(String encryptedMessage) {
        this.encryptedMessage = encryptedMessage;
    }
}
