package yesa.student.koramail.utils;

import android.content.Context;
import android.content.SharedPreferences;

public class Preference {
    private SharedPreferences preferences;

    public Preference(Context context) {
        String PREF_NAME = "pref.koramail";
        int PREF_CODE = 0;
        preferences = context.getSharedPreferences(PREF_NAME, PREF_CODE);
    }

    public void saveEmail(String email) {
        SharedPreferences.Editor edit = preferences.edit();
        edit.putString("email", email);
        edit.apply();
    }

    public String getEmail() {
        return preferences.getString("email", "");
    }

    public void removeEmail() {
        SharedPreferences.Editor edit = preferences.edit();
        edit.remove("email");
        edit.apply();
    }
}
