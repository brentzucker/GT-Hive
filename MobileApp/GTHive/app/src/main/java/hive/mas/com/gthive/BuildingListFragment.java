package hive.mas.com.gthive;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
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
        private TextView mIdTextView;

        public BuildingHolder(View itemView) {
            super(itemView);
            itemView.setOnClickListener(this);

            mNameTextView = (TextView) itemView.findViewById(R.id.list_item_building_name_text_view);
            mIdTextView = (TextView) itemView.findViewById(R.id.list_item_building_id_text_view);
        }

        public void bindBuilding(Building building) {
            mBuilding = building;
            mNameTextView.setText(mBuilding.getName());
            mIdTextView.setText(mBuilding.getId());
        }

            @Override
            public void onClick(View v) {
                Intent intent = BuildingPagerActivity.newIntent(getActivity(), mBuilding.getId());
                startActivity(intent);
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
}
