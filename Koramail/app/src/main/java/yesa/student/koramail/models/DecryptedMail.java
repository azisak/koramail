package yesa.student.koramail.models;

import com.google.gson.annotations.SerializedName;

public class DecryptedMail {
    @SerializedName("decrypted")
    private String decryptedMessage;

    public String getDecryptedMessage() {
        return decryptedMessage;
    }

    public void setDecryptedMessage(String decryptedMessage) {
        this.decryptedMessage = decryptedMessage;
    }
}
