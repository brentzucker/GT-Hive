package hive.mas.com.gthive;

import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;

import java.util.ArrayList;
import java.util.List;

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


        /* Draw Line Graph */

        // List<Integer> todaysCrowdValues = mBuilding.getTodaysCrowdValues();
        // List<Integer> rodCrowdValues = mBuilding.getRodCrowdValues();
        // temporarily using random numbers
        List<Integer> todaysCrowdValues = new ArrayList<>();
        List<Integer> rodCrowdValues = new ArrayList<>();
        for (int i = 0; i <= 12; i++) todaysCrowdValues.add( (int)(100 * (Math.random() * 10)));
        for (int i = 0; i <= 12; i++) rodCrowdValues.add( (int)(100 * (Math.random() * 10)));

        drawLineChart(v, todaysCrowdValues, rodCrowdValues);

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

    public void drawLineChart(View v, List<Integer> todaysCrowdValues, List<Integer> rodCrowdValues) {

        /* Create data entries1 and labels for todaysCrowd Values*/
        ArrayList<Entry> entries1 = new ArrayList<>();
        ArrayList<String> labels = new ArrayList<>();
        for (int hour = 0; hour < todaysCrowdValues.size(); hour++) {
            entries1.add(new Entry(todaysCrowdValues.get(hour), hour));
            labels.add("" + hour);
        }

        /* Create data entries2 and labels for rodCrowdValues Values*/
        ArrayList<Entry> entries2 = new ArrayList<>();
        for (int hour = 0; hour < rodCrowdValues.size(); hour++) {
            entries2.add(new Entry(rodCrowdValues.get(hour), todaysCrowdValues.size() + 12));
            labels.add("" + (hour + 12));
        }

        // Create dataset from data entries1
        LineDataSet dataset1 = new LineDataSet(entries1, "Todays Crowd Values");
        LineDataSet dataset2 = new LineDataSet(entries2, "Predicted Crowd Values");

        // Set the color for this dataset
        dataset1.setColor(Color.rgb(0, 37, 76)); // GT Navy
        dataset2.setColor(Color.rgb(238, 178, 17)); // Buzz Gold

        /* Create the chart */
        LineChart chart = (LineChart) v.findViewById(R.id.chart);

        ArrayList<LineDataSet> dataSets = new ArrayList<LineDataSet>();
        dataSets.add(dataset1);
        dataSets.add(dataset2);

        LineData data = new LineData(labels, dataSets);
        chart.setData(data);

        chart.setDescription("Today's Crowd Level");

        // animations
        chart.animateY(1000);
    }
}
