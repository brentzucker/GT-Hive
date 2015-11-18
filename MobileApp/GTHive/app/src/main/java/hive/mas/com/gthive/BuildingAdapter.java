package hive.mas.com.gthive;

import android.app.Activity;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.List;

/**
 * Created by bvz on 11/18/15.
 */
public class BuildingAdapter extends RecyclerView.Adapter<BuildingHolder> {

    private Activity mActivity;

    private List<Building> mBuildings;

    public BuildingAdapter(Activity activity, List<Building> buildings) {
        mActivity = activity;
        mBuildings = buildings;
    }

    @Override
    public BuildingHolder onCreateViewHolder(ViewGroup parent, int viewType) {

        LayoutInflater layoutInflater = LayoutInflater.from(mActivity);
        View view = layoutInflater.inflate(R.layout.list_item_building, parent, false);
        return new BuildingHolder(mActivity, view);
    }

    @Override
    public void onBindViewHolder(BuildingHolder holder, int position) {
        Building building = mBuildings.get(position);
        holder.bindBuilding(building);
    }

    @Override
    public int getItemCount() {
        return mBuildings.size();
    }
}