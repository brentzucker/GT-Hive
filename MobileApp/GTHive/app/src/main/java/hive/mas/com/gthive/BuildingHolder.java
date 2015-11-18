package hive.mas.com.gthive;

import android.app.Activity;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.TextView;

/**
 * Created by bvz on 11/18/15.
 */
// TODO: Fix loading occupancies / updating UI bug
public class BuildingHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

    private Activity mActivity;

    private Building mBuilding;

    private TextView mNameTextView;
    private TextView mOccupancyTextView;
    private TextView mPercentageOccupiedTextView;
    private CheckBox mFavoriteCheckbox;

    public BuildingHolder(Activity activity, View itemView) {
        super(itemView);
        itemView.setOnClickListener(this);

        mActivity = activity;
        mNameTextView = (TextView) itemView.findViewById(R.id.list_item_building_name_text_view);
        mOccupancyTextView = (TextView) itemView.findViewById(R.id.list_item_building_occupancy_text_view);
        mPercentageOccupiedTextView = (TextView) itemView.findViewById(R.id.percentage_occupied_text_view);
        mFavoriteCheckbox = (CheckBox) itemView.findViewById(R.id.favorite_button);
    }

    public void bindBuilding(Building building) {
        mBuilding = building;
        mNameTextView.setText(mBuilding.getName());
        mOccupancyTextView.setText("" + mBuilding.getOccupancy());

        setFavoriteCheckbox();

        mFavoriteCheckbox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

                Favorites favorites = Favorites.get(mActivity);
                if (isChecked) {
                    favorites.addBuildingId(mBuilding.getBId());
                } else {
                    favorites.removeBuildingId(mBuilding.getBId());
                }
            }
        });

        setPercentageOccupiedTextView(((int) (Math.random() * 100)));
    }

    @Override
    public void onClick(View v) {
        Intent intent = BuildingPagerActivity.newIntent(mActivity, mBuilding.getId());
        mActivity.startActivity(intent);
    }

    public void setPercentageOccupiedTextView(int occupancyPercentage) {

        int color;
        switch (occupancyPercentage / 10) {
            case 10: color = R.color.Red10;
                break;
            case 9:  color = R.color.Red9;
                break;
            case 8:  color = R.color.Red8;
                break;
            case 7:  color = R.color.Yellow7;
                break;
            case 6:  color = R.color.Yellow6;
                break;
            case 5:  color = R.color.Yellow5;
                break;
            case 4:  color = R.color.Yellow4;
                break;
            case 3:  color = R.color.Green3;
                break;
            case 2:  color = R.color.Green2;
                break;
            case 1:  color = R.color.Green1;
                break;
            case 0:  color = R.color.Green1;
                break;
            default: color = R.color.Red11;
                break;
        }

        mPercentageOccupiedTextView.setText("" + occupancyPercentage);

        Drawable background = mPercentageOccupiedTextView.getBackground();

        // http://stackoverflow.com/questions/17823451/set-android-shape-color-programmatically
        if (background instanceof GradientDrawable) {
            // cast to 'GradientDrawable'
            GradientDrawable gradientDrawable = (GradientDrawable) background;
            gradientDrawable.setColor(ContextCompat.getColor(mActivity, color));
        } else if (background instanceof ShapeDrawable) {
            ShapeDrawable shapeDrawable = (ShapeDrawable) background;
            shapeDrawable.getPaint().setColor(ContextCompat.getColor(mActivity, color));
        } else {
            Log.e("PercentageOccupiedTextView", "not selected");
        }
    }

    public void setFavoriteCheckbox() {

        mFavoriteCheckbox.setChecked(false);
        if (mBuilding.isFavorite(mActivity)) {
            mFavoriteCheckbox.setChecked(true);
        }
    }
}