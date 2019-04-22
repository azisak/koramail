package yesa.student.koramail.networks;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import yesa.student.koramail.utils.Globals;

public class RetrofitInstance {

    private static final Integer connectTimeout = 600;
    private static final Integer readTimeout = 600;
    private static final Integer writeTimeout = 600;

    public static Retrofit getInstance() {
        return new Retrofit.Builder().client(getOkHttpClient()).baseUrl(Globals.BASE_ENDPOINT_URL).addConverterFactory(
                GsonConverterFactory.create()).build();
    }

    private static OkHttpClient getOkHttpClient() {
        return new OkHttpClient.Builder()
                .connectTimeout(connectTimeout, TimeUnit.SECONDS)
                .writeTimeout(writeTimeout, TimeUnit.SECONDS)
                .readTimeout(readTimeout, TimeUnit.SECONDS)
                .build();
    }
}