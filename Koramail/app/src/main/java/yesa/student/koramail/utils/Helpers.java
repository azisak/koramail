package yesa.student.koramail.utils;

import android.content.Context;
import android.content.DialogInterface;
import android.os.Environment;
import android.support.v7.app.AlertDialog;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class Helpers {

    public static void showWarning(Context context, String message) {
        new AlertDialog.Builder(context)
                .setTitle("WARNING")
                .setMessage(message)
                .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                })
                .show();
    }

    public static String generateSignedContent(String content, String signature) {
        String startDelimiter = "----- BEGIN PGP SIGNATURE -----\n";
        String endDelimiter = "----- END PGP SIGNATURE -----\n";
        return content + "\n\n" + startDelimiter + signature + "\n" + endDelimiter;
    }

    public static String getSignatureFromSignedContent(String signedContent) {
        String startDelimiter = "----- BEGIN PGP SIGNATURE -----\n";
        String endDelimiter = "----- END PGP SIGNATURE -----\n";
        int endIndexStartDelimiter = signedContent.lastIndexOf(startDelimiter);
        int startIndexEndDelimiter = signedContent.indexOf(endDelimiter);
        return signedContent.substring(endIndexStartDelimiter + 32, startIndexEndDelimiter - 1);
    }

    public static String getContentFromSignedContent(String signedContent) {
        String startDelimiter = "----- BEGIN PGP SIGNATURE -----\n";
        int startIndexStartDelimiter = signedContent.indexOf(startDelimiter);
        return signedContent.substring(0, startIndexStartDelimiter - 2);
    }

    public static String normalizeText(String text) {
        int standardLength = 30;
        if (text.length() > standardLength) {
            text = text.substring(0, standardLength - 1) + "...";
        }
        return text;
    }

    public File getTemporaryFile() {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
        String fileName = "temp_" + timeStamp;
        return new File(Environment.getExternalStorageDirectory(), fileName);
    }
}
