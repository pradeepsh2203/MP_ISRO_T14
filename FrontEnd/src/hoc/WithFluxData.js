import { ResultContext } from "context/ResultContext";
import { useContext } from "react";

const WithFluxData = (WrappedComponent) => {
	const convertSorted = (arr) => {
		arr.sort((a, b) => a.time - b.time);
	};
	return (props) => {
		// eslint-disable-next-line react-hooks/rules-of-hooks
		const context = useContext(ResultContext);
		console.log(context.flux_a);
		const masterChart = context.comb;
		convertSorted(masterChart);
		const AChart = context.flux_a;
		convertSorted(AChart);
		const BChart = context.flux_b;
		convertSorted(BChart);
		const CChart = context.flux_c;
		convertSorted(CChart);
		const XChart = context.flux_x;
		convertSorted(XChart);
		const MChart = context.flux_m;
		convertSorted(MChart);

		console.log("MasterChart", masterChart);
		return (
			<WrappedComponent
				{...props}
				masterChart={masterChart}
				AChart={AChart}
				BChart={BChart}
				CChart={CChart}
				XChart={XChart}
				MChart={MChart}
			/>
		);
	};
};

export default WithFluxData;
