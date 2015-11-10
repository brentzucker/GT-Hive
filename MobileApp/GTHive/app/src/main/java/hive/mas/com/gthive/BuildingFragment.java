package hive.mas.com.gthive;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

/**
 * Created by bvz on 11/2/15.
 */
public class BuildingFragment extends android.support.v4.app.Fragment {

    private static final String ARG_BUILDING_ID = "building_id";

    private Building mBuilding;
    private TextView mNameTextView;
    private TextView mOccupancyTextView;
    private TextView mFirstBestTimeTextView;
    private TextView mSecondBestTimeTextView;
    private TextView mThirdBestTimeTextView;
    private LinearLayout mFloorsLinearLayout;

    public static BuildingFragment newInstance(String buildingId) {
        Bundle args = new Bundle();
        args.putSerializable(ARG_BUILDING_ID, buildingId);

        BuildingFragment fragment = new BuildingFragment();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String buildingId = (String) getArguments().getSerializable(ARG_BUILDING_ID);
        mBuilding = Campus.get(getActivity()).getBuilding(buildingId);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_building, container, false);

        getActivity().setTitle(mBuilding.getName());

        mNameTextView = (TextView) v.findViewById(R.id.building_name);
        mNameTextView.setText(mBuilding.getName());

        mOccupancyTextView = (TextView) v.findViewById(R.id.occupancy);
        mOccupancyTextView.setText("" + mBuilding.getOccupancy());

        // Temporarily use fake numbers for best times
        mFirstBestTimeTextView = (TextView) v.findViewById(R.id.first_best_time_text_view);
        mFirstBestTimeTextView.setText("8am");

        mSecondBestTimeTextView = (TextView) v.findViewById(R.id.second_best_time_text_view);
        mSecondBestTimeTextView.setText("1pm");

        mThirdBestTimeTextView = (TextView) v.findViewById(R.id.third_best_time_text_view);
        mThirdBestTimeTextView.setText("7pm");

        mFloorsLinearLayout = (LinearLayout) v.findViewById(R.id.floors_linear_layout);
        for (Floor f : mBuilding.getFloors()) {

            View listItemFloor = inflater.inflate(R.layout.list_item_floor, null, false);

            TextView floorNumberTextView = (TextView) listItemFloor.findViewById(R.id.floor_number_text_view);
            floorNumberTextView.setText("Floor " + f.getFloorNumber());

            TextView floorOccupancyTextView = (TextView) listItemFloor.findViewById(R.id.floor_occupancy_text_view);
            floorOccupancyTextView.setText("" + f.getOccupancy());

            mFloorsLinearLayout.addView(listItemFloor);
        }

        return v;
    }
}
