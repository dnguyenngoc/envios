import { configureStore } from "@reduxjs/toolkit";
import restoresReducer from "./features/RestoreSlide";

export const store = configureStore({
	reducer: {
		restores: restoresReducer,
	},
});
