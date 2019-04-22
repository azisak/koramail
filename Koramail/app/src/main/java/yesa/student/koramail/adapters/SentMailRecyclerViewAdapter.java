package yesa.student.koramail.adapters;

import android.content.Context;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;

import butterknife.BindView;
import butterknife.ButterKnife;

import java.util.ArrayList;

import yesa.student.koramail.R;
import yesa.student.koramail.activities.ViewMailActivity;
import yesa.student.koramail.models.Mail;
import yesa.student.koramail.utils.Globals;
import yesa.student.koramail.utils.Helpers;

public class SentMailRecyclerViewAdapter extends RecyclerView.Adapter<SentMailRecyclerViewAdapter.SentMailViewHolder> {

    private ArrayList<Mail> mails;
    private Context context;

    public SentMailRecyclerViewAdapter(ArrayList<Mail> mails, Context context) {
        this.mails = mails;
        this.context = context;
    }

    @NonNull
    @Override
    public SentMailViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View view = LayoutInflater.from(viewGroup.getContext())
                .inflate(R.layout.item_mail, viewGroup, false);
        return new SentMailRecyclerViewAdapter.SentMailViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull SentMailViewHolder sentMailViewHolder, int i) {
        String subject = Helpers.normalizeText(mails.get(i).getSubject());
        sentMailViewHolder.containerSubject.setText(subject);

        String content = Helpers.normalizeText(mails.get(i).getContent());
        sentMailViewHolder.containerContent.setText(content);

        final int position = i;
        sentMailViewHolder.layoutItemMail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Globals.DATA_VIEWED_EMAIL = mails.get(position);
                Intent viewMail = new Intent(context, ViewMailActivity.class);
                context.startActivity(viewMail);
            }
        });
    }

    @Override
    public int getItemCount() {
        return mails.size();
    }

    class SentMailViewHolder extends RecyclerView.ViewHolder {
        @BindView(R.id.layout_item_mail)
        RelativeLayout layoutItemMail;
        @BindView(R.id.container_subject)
        TextView containerSubject;
        @BindView(R.id.container_content)
        TextView containerContent;

        SentMailViewHolder(@NonNull View itemView) {
            super(itemView);
            ButterKnife.bind(this, itemView);
        }
    }
}
