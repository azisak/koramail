package yesa.student.koramail.fragments;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import butterknife.BindView;
import butterknife.ButterKnife;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import yesa.student.koramail.R;
import yesa.student.koramail.adapters.SentMailRecyclerViewAdapter;
import yesa.student.koramail.models.Mail;
import yesa.student.koramail.networks.APIServices;
import yesa.student.koramail.networks.RetrofitInstance;
import yesa.student.koramail.utils.Preference;


public class SentMailFragment extends Fragment {

    @BindView(R.id.recyclerview_sent_mail)
    RecyclerView recyclerView;

    private ArrayList<Mail> mails;
    private SentMailRecyclerViewAdapter sentMailRecyclerViewAdapter;
    private APIServices apiServices;
    private Preference preference;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sent_mail, container, false);
        ButterKnife.bind(this, view);

        mails = new ArrayList<>();
        apiServices = RetrofitInstance.getInstance().create(APIServices.class);
        preference = new Preference(getContext());

        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        sentMailRecyclerViewAdapter = new SentMailRecyclerViewAdapter(mails, getContext());
        recyclerView.setAdapter(sentMailRecyclerViewAdapter);

        getMails();

        return view;
    }

    @Override
    public void setUserVisibleHint(boolean isVisibleToUser) {
        super.setUserVisibleHint(isVisibleToUser);
        if (isVisibleToUser) {
            try {
                getMails();
            } catch (Exception ignored) {}
        }
    }

    private void getMails() {
        Call<List<Mail>> get = apiServices.getSentMails(preference.getEmail());
        get.enqueue(new Callback<List<Mail>>() {
            @Override
            public void onResponse(Call<List<Mail>> call, Response<List<Mail>> response) {
                List<Mail> _mails = response.body();
                if (_mails == null) return;

                mails.clear();
                mails.addAll(_mails);
                sentMailRecyclerViewAdapter.notifyDataSetChanged();
            }

            @Override
            public void onFailure(Call<List<Mail>> call, Throwable t) {
                Toast.makeText(getContext(), t.getLocalizedMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}
