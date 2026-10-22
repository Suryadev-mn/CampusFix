import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Building2, Plus, Layers, MapPin, Loader2, CheckCircle2 } from 'lucide-react';
import { departmentService } from '../services/api';

export const AdminDepartmentsPage = () => {
  const [departments, setDepartments] = useState([]);
  const [buildings, setBuildings] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Department Form
  const [deptName, setDeptName] = useState('');
  const [deptCode, setDeptCode] = useState('');
  const [deptCategory, setDeptCategory] = useState('academic');
  const [deptDesc, setDeptDesc] = useState('');
  const [addingDept, setAddingDept] = useState(false);

  // New Building Form
  const [bldgName, setBldgName] = useState('');
  const [bldgCode, setBldgCode] = useState('');
  const [bldgFloors, setBldgFloors] = useState(3);
  const [addingBldg, setAddingBldg] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [dList, bList] = await Promise.all([
        departmentService.getDepartments(),
        departmentService.getBuildings(),
      ]);
      setDepartments(dList);
      setBuildings(bList);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddDept = async (e) => {
    e.preventDefault();
    if (!deptName || !deptCode) return;
    setAddingDept(true);
    try {
      const created = await departmentService.createDepartment({
        name: deptName.trim(),
        code: deptCode.trim().toUpperCase(),
        category: deptCategory,
        description: deptDesc.trim(),
      });
      setDepartments((prev) => [...prev, created]);
      setDeptName('');
      setDeptCode('');
      setDeptCategory('academic');
      setDeptDesc('');
    } catch (err) {
      console.error(err);
    } finally {
      setAddingDept(false);
    }
  };

  const handleAddBldg = async (e) => {
    e.preventDefault();
    if (!bldgName || !bldgCode) return;
    setAddingBldg(true);
    try {
      const created = await departmentService.createBuilding({
        name: bldgName.trim(),
        code: bldgCode.trim().toUpperCase(),
        total_floors: Number(bldgFloors),
      });
      setBuildings((prev) => [...prev, created]);
      setBldgName('');
      setBldgCode('');
      setBldgFloors(3);
    } catch (err) {
      console.error(err);
    } finally {
      setAddingBldg(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Campus Departments & Buildings
        </h1>
        <p className="text-xs text-slate-500">
          Configure campus physical structure, academic wings, and facility divisions
        </p>
      </div>

      {/* Departments Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Department List (2 cols) */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-900">Active Campus Departments</h3>
            <span className="text-xs font-mono text-slate-400">{departments.length} divisions</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {departments.map((dept) => (
              <div
                key={dept.id}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-bold font-mono text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                      {dept.code}
                    </span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                      dept.category === 'academic'
                        ? 'bg-purple-100 text-purple-700'
                        : 'bg-emerald-100 text-emerald-700'
                    }`}>
                      {dept.category === 'academic' ? 'Academic Branch' : 'Facility Division'}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400">
                    {dept.issue_count || 0} issues
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-900">{dept.name}</h4>
                <p className="text-xs text-slate-500 line-clamp-2">{dept.description || 'Facility division'}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Add Department Form (1 col) */}
        <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
            Add New Department
          </h3>
          <form onSubmit={handleAddDept} className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Department Name</label>
              <input
                type="text"
                required
                placeholder="e.g. Mechanical Workshop"
                value={deptName}
                onChange={(e) => setDeptName(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Code</label>
              <input
                type="text"
                required
                placeholder="e.g. MECH"
                value={deptCode}
                onChange={(e) => setDeptCode(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Department Type</label>
              <select
                value={deptCategory}
                onChange={(e) => setDeptCategory(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              >
                <option value="academic">Academic Branch (for Students)</option>
                <option value="facility">Facility / Maintenance (for Staff)</option>
              </select>
            </div>
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Description</label>
              <textarea
                rows={2}
                placeholder="Brief summary of responsibilities..."
                value={deptDesc}
                onChange={(e) => setDeptDesc(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <button
              type="submit"
              disabled={addingDept}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-colors shadow-xs"
            >
              {addingDept ? 'Adding...' : 'Create Department'}
            </button>
          </form>
        </div>
      </div>

      {/* Buildings Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Building List (2 cols) */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-900">Campus Buildings & Blocks</h3>
            <span className="text-xs font-mono text-slate-400">{buildings.length} buildings</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {buildings.map((bldg) => (
              <div
                key={bldg.id}
                className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold font-mono text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">
                    {bldg.code}
                  </span>
                  <span className="text-[11px] text-slate-500 font-medium">
                    {bldg.total_floors} Floors • {bldg.total_classrooms || bldg.classrooms?.length || 0} Rooms
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-900">{bldg.name}</h4>
                <p className="text-xs text-slate-500">{bldg.description || 'Academic & facility block'}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Add Building Form (1 col) */}
        <div className="bg-white rounded-3xl border border-slate-200/80 shadow-md p-6 space-y-4">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">
            Add New Building
          </h3>
          <form onSubmit={handleAddBldg} className="space-y-3 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Building Name</label>
              <input
                type="text"
                required
                placeholder="e.g. Vikram Sarabhai Center"
                value={bldgName}
                onChange={(e) => setBldgName(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Code</label>
              <input
                type="text"
                required
                placeholder="e.g. VSC"
                value={bldgCode}
                onChange={(e) => setBldgCode(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 uppercase mb-1">Total Floors</label>
              <input
                type="number"
                min="1"
                max="20"
                value={bldgFloors}
                onChange={(e) => setBldgFloors(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <button
              type="submit"
              disabled={addingBldg}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-colors shadow-xs"
            >
              {addingBldg ? 'Adding...' : 'Create Building'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
export default AdminDepartmentsPage;
