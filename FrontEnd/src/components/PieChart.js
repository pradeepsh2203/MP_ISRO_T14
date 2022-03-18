import { ResultContext } from "context/ResultContext";
import { useContext } from "react";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer } from "recharts";

const Piechart = () => {
	const context = useContext(ResultContext);
	let a = 0,
		b = 0,
		c = 0,
		x = 0,
		m = 0;

	for (let ind in context.comb) {
		if (context.comb[ind].flux_a !== 0) a++;
		else if (context.comb[ind].flux_b !== 0) b++;
		else if (context.comb[ind].flux_c !== 0) c++;
		else if (context.comb[ind].flux_x !== 0) x++;
		else m++;
	}

	const data = [
		{ type: "A", value: a },
		{ type: "B", value: b },
		{ type: "C", value: c },
		{ type: "X", value: x },
		{ type: "M", value: m },
	];
	const colors = ["#6bd098", "#f17e5d", "#fcc468", "#d296da", "#72b3b3"];
	console.log(data);
	return (
		<ResponsiveContainer width="100%" height="100%">
			<PieChart>
				<Pie
					data={data}
					cx="50%"
					cy={"50%"}
					dataKey="value"
					nameKey="type"
					fill="#fe7d5a"
					outerRadius={100}
				>
					{data.map((entry, index) => (
						<Cell fill={colors[index]} />
					))}
				</Pie>
				<Legend />
			</PieChart>
		</ResponsiveContainer>
	);
};

export default Piechart;
