<script setup lang="ts">
import Cookies from "universal-cookie"
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const cookies = new Cookies()
const router = useRouter()
const name = ref('')

const selectedFile = ref(null)

const metrics = ref(null)

const logoutView = () => {
	fetch("/logout/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": cookies.get("csrftoken"),
		},
		credentials: "same-origin",
	})
		.then((res) => res.json())
		.then((data) => {
			router.push({ name: 'Login' })
		})
}

const whoamiView = () => {
	fetch("/whoami/", {
		credentials: "same-origin",
	})
		.then((res) => res.json())
		.then((data) => {
			name.value = data.username
		})
}

const handleFileSelect = (event) => {
	const target = event.target as HTMLInputElement

	selectedFile.value = target.files[0]

	const formData = new FormData()
	formData.append('file', selectedFile.value)

	fetch('/upload/', {
		method: "POST",
		headers: {
			"X-CSRFToken": cookies.get("csrftoken"),
		},
		credentials: "same-origin",
    	body: formData
	})
    	.then((res) => res.json())
    	.then((data) => {
    	metrics.value = data
    })
}

onMounted(() => {
	whoamiView()
})

</script>

<template>
	<div class="mx-auto text-center" style="max-width: 400px;">
		<p>Welcome, {{ name }}!</p>
		<button @click="logoutView">Logout</button>
	</div>
	<div class="mx-auto text-center" style="max-width: 400px;">
		<div>
			<label for="file-input" class="btn">Upload File</label>
			<input
				id="file-input"
				type="file"
				accept=".pdb"
				@change="handleFileSelect"
				hidden
			/>
		</div>
	</div>
	<div>
		<!-- ADD: Metrics Display Section -->
		<div v-if="metrics" class="metrics-container">
			<h3>PDB Analysis Results</h3>
			
			<!-- Main Score -->
			<div class="score-section">
				<p><strong>Approximate PTM Score:</strong> {{ metrics.approximate_ptm_score }}</p>
				<p><strong>Median PLDDT:</strong> {{ metrics.median_plddt }}</p>
			</div>

			<div class="metrics">
				<h4>Metrics</h4>
				<div class="metric-grid">
					<div class="metric-card">
						<label>Mean PLDDT</label>
						<span>{{ metrics.metrics.mean_plddt }}</span>
					</div>
					
					<div class="metric-card">
						<label>Percent Below 50</label>
						<span>{{ `${metrics.metrics.percent_below_50}%` }}</span>
					</div>
					
					<div class="metric-card">
						<label>Percent Below 70</label>
						<span>{{ `${metrics.metrics.percent_below_70}%` }}</span>
					</div>

					<div class="metric-card">
						<label>Longest Low Confidence Segment</label>
						<span>{{ metrics.metrics.longest_low_confidence_segment }}</span>
					</div>
				</div>
			</div>

			<!-- Notes -->
			<div v-if="metrics.notes && metrics.notes.length > 0" class="notes-section">
				<h4>Notes</h4>
				<ul>
					<li v-for="note in metrics.notes" :key="note">{{ note }}</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<style scoped>
.btn {
	padding: 8px 16px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: inline-block;
}

.btn:hover {
	background-color: #0056b3;
}

.metrics-container {
	margin-top: 20px;
	padding: 20px;
	border: 1px solid #ddd;
	border-radius: 8px;
	background-color: #f9f9f9;
}

.score-section {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	padding: 20px;
	border-radius: 10px;
	margin-bottom: 20px;
	text-align: center;
}

.score-value {
	font-size: 2em;
	font-weight: bold;
	margin: 10px 0;
}

.detailed-metrics {
	background: white;
	padding: 15px;
	border-radius: 8px;
	margin-bottom: 15px;
}

.metric-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
	gap: 10px;
	margin-top: 10px;
}

.metric-card {
	padding: 10px;
	background: #f8f9fa;
	border-radius: 4px;
	border-left: 3px solid #007bff;
}

.metric-card label {
	display: block;
	font-weight: bold;
	color: #666;
	margin-bottom: 5px;
	font-size: 0.9em;
}

.metric-card span {
	font-size: 1.2em;
	font-weight: bold;
	color: #333;
}

.notes-section {
	background: #fff3cd;
	padding: 15px;
	border-radius: 8px;
	border: 1px solid #ffeaa7;
}

.notes-section h4 {
	margin-top: 0;
	color: #856404;
}

.notes-section ul {
	margin: 0;
	padding-left: 20px;
}
</style>