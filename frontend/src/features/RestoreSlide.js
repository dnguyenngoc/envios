import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  restores: [],
  process: {},

};

export const restoreSlice = createSlice({
  name: "restores",
  initialState,
  reducers: {
    addRestore: (state, action) => {
	  state.restores.push(action.payload);
	},
	deleteRestore: (state, action) => {
	  state.restores = state.restores.filter((restore) => restore.id !== action.payload);
	},
	updateRestore: (state, action) => {
	  let check = state.restores.map(restore=>{
		return restore.id
	  })
      action.payload.forEach(restore => {
    	if (check.indexOf(restore.id) === -1) {
          state.restores.push(restore)
    	}
	  })
	},
	addProcess: (state, action) => {
		state.process[action.payload.deviceId] = action.payload
	},
	deleteProcess: (state, action) => {
		delete state.process[action.payload]
	}
  }
});

export const { addRestore, deleteRestore, updateRestore, addProcess, deleteProcess } = restoreSlice.actions;
export default restoreSlice.reducer;