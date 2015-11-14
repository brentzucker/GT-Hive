package hive.mas.com.gthive;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;


/**
 * Created by bvz on 11/1/15.
 */
public class BuildingListFragment extends Fragment {

    private RecyclerView mBuildingRecyclerView;
    private BuildingAdapter mAdapter;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setHasOptionsMenu(true);

        // Load Buildings Occupancies from API
        setRetainInstance(true);
        new FetchBuildingsTask("BuildingOccupancies", Campus.get(getActivity())).execute();

        // Load Floor Occupancies from API
        new FetchBuildingsTask("FloorOccupancies", Campus.get(getActivity())).execute();
    }

    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        super.onCreateOptionsMenu(menu, inflater);
        inflater.inflate(R.menu.fragment_building_list, menu);
    }


    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstance) {
        View view = inflater.inflate(R.layout.fragment_building_list, container, false);

        mBuildingRecyclerView = (RecyclerView) view.findViewById(R.id.building_recycler_view);
        mBuildingRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        return view;
    }

    @Override
    public void onResume() {
        super.onResume();
        updateUI();
    }

    private void updateUI() {

        Campus campus = Campus.get(getActivity());
        List<Building> buildings = campus.getBuildings();

        if (mAdapter == null) {
            mAdapter = new BuildingAdapter(buildings);
            mBuildingRecyclerView.setAdapter(mAdapter);
        } else {
            mAdapter.notifyDataSetChanged();
        }
    }

    private class BuildingHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        private Building mBuilding;

        private TextView mNameTextView;
        private TextView mOccupancyTextView;
        private TextView mPercentageOccupiedTextView;
        private Drawable mPercentageOccupiedBoxDrawable;
        private ImageView mStatusView;

        public BuildingHolder(View itemView) {
            super(itemView);
            itemView.setOnClickListener(this);

            mNameTextView = (TextView) itemView.findViewById(R.id.list_item_building_name_text_view);
            mOccupancyTextView = (TextView) itemView.findViewById(R.id.list_item_building_occupancy_text_view);
            mPercentageOccupiedTextView = (TextView) itemView.findViewById(R.id.percentage_occupied_text_view);
            mStatusView = (ImageView) itemView.findViewById(R.id.list_item_occupancy_status);
//            mPercentageOccupiedBoxDrawable = (Drawable) itemView.findViewById(R.drawable.percentage_occupied_box_drawable);
        }

        public void bindBuilding(Building building) {
            mBuilding = building;
            mNameTextView.setText(mBuilding.getName());
            mOccupancyTextView.setText("" + mBuilding.getOccupancy());

            setPercentageOccupiedTextView(((int) (Math.random() * 100)));

            CharSequence text = mOccupancyTextView.getText();
            int number = Integer.parseInt(text.toString());
            if (number <= 10) { //instead of 10 need to use capacity of building
                mStatusView.setImageResource(R.drawable.ic_thumbs_up);
//                mStatusView.setImageDrawable(getResources().getDrawable(R.drawable.percentage_occupied_box_drawable));
            } else {
                mStatusView.setImageResource(R.drawable.ic_thumbs_down);
            }
        }

        @Override
        public void onClick(View v) {
            Intent intent = BuildingPagerActivity.newIntent(getActivity(), mBuilding.getId());
            startActivity(intent);
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
                gradientDrawable.setColor(ContextCompat.getColor(getContext(), color));
            } else if (background instanceof ShapeDrawable) {
                ShapeDrawable shapeDrawable = (ShapeDrawable) background;
                shapeDrawable.getPaint().setColor(ContextCompat.getColor(getContext(), color));
            } else {
                Log.e("PercentageOccupiedTextView", "not selected");
            }
        }
    }

    private class BuildingAdapter extends RecyclerView.Adapter<BuildingHolder> {

        private List<Building> mBuildings;

        public BuildingAdapter(List<Building> buildings) {
            mBuildings = buildings;
        }

        @Override
        public BuildingHolder onCreateViewHolder(ViewGroup parent, int viewType) {

            LayoutInflater layoutInflater = LayoutInflater.from(getActivity());
            View view = layoutInflater.inflate(R.layout.list_item_building, parent, false);
            return new BuildingHolder(view);
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

    private class FetchBuildingsTask extends AsyncTask<Void, Void, Campus> {

        Campus campus;
        String taskType;

        protected FetchBuildingsTask(String taskType, Campus campus) {
            this.campus = campus;
            this.taskType = taskType;
        }

        @Override
        protected Campus doInBackground(Void... params) {
            if (taskType.equals("BuildingOccupancies")) {
                return new APIFetcher().fetchBuildingOccupancies(this.campus);
            } else if (taskType.equals("FloorOccupancies")) {
                return new APIFetcher().fetchFloorOccupancies(this.campus);
            } else
                return campus;
        }

        @Override
        protected void onPostExecute(Campus campus) {
            updateUI();
        }
    }
}
