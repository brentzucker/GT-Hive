package hive.mas.com.gthive;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.List;


/**
 * Created by bvz on 11/1/15.
 */
public class BuildingListFragment extends Fragment {

    private RecyclerView mBuildingRecyclerView;
    private BuildingAdapter mAdapter;

    //adding ability to use tabs
    public static final String ARG_PAGE = "ARG_PAGE";
    private int mPage;

    public static BuildingListFragment newInstance(int page) {
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, page);
        BuildingListFragment fragment = new BuildingListFragment();
        fragment.setArguments(args);
        return fragment;
    }
    //ended ability to use tabs

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


    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstance) {
        View view = inflater.inflate(R.layout.fragment_menu, container, false);

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
            mAdapter = new BuildingAdapter(getActivity(), buildings);
            mBuildingRecyclerView.setAdapter(mAdapter);
        } else {
            mAdapter.notifyDataSetChanged();
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