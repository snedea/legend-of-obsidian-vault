declare global {
  interface Window {
    electronAPI?: {
      selectVaultFolder: () => Promise<string | null>;
      getBackendPort: () => Promise<number>;
    };
    __BACKEND_PORT__?: number;
  }
}

const BASE_URL = window.__BACKEND_PORT__
  ? `http://127.0.0.1:${window.__BACKEND_PORT__}`
  : 'http://127.0.0.1:8742';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

function get<T>(path: string): Promise<T> {
  return request<T>(path);
}

function post<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, {
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}

// ---- Health ----

export function healthCheck() {
  return get<{ status: string; version: string }>('/api/health');
}

// ---- Character ----

export interface Character {
  name: string;
  gender: string;
  class_type: string;
  level: number;
  experience: number;
  hitpoints: number;
  max_hitpoints: number;
  forest_fights: number;
  player_fights: number;
  gold: number;
  bank_gold: number;
  weapon: string;
  weapon_num: number;
  armor: string;
  armor_num: number;
  strength: number;
  defense: number;
  charm: number;
  gems: number;
  horse: boolean;
  fairy_blessing: boolean;
  fairy_lore: boolean;
  alive: boolean;
  days_played: number;
  skill_uses: number;
  attack_power: number;
  defense_power: number;
  death_knight_points: number;
  mystical_points: number;
  thieving_points: number;
  skills_used_today: number;
  is_werewolf: boolean;
  werewolf_transformations: number;
  dragon_kills: number;
  total_kills: number;
  times_won_game: number;
  stored_gold: number;
  stored_gems: number;
  spirit_level: string;
  children: number;
  horse_name: string;
  bank_robberies_today: number;
  successful_robberies: number;
  cavern_searches_today: number;
  married: boolean;
  married_to: string;
  inn_room: boolean;
  flirted_violet: boolean;
  laid_today: boolean;
}

export function createCharacter(name: string, gender: string, classType: string) {
  return post<Character>('/api/character/create', { name, gender, class_type: classType });
}

export function listCharacters() {
  return get<{ characters: Character[] }>('/api/character/list');
}

export function selectCharacter(name: string) {
  return post<Character>(`/api/character/select/${encodeURIComponent(name)}`);
}

export function getCurrentCharacter() {
  return get<Character>('/api/character/current');
}

// ---- Combat ----

export interface Enemy {
  name: string;
  hitpoints: number;
  max_hitpoints: number;
  attack: number;
  gold_reward: number;
  exp_reward: number;
  level: number;
  note_title: string;
  note_content: string;
  backstory: string;
  knowledge_domain: string;
  description: string;
  weapon: string;
  armor: string;
  encounter_narrative: string;
  combat_phrases: string[];
  defeat_message: string;
  victory_message: string;
}

export interface CombatState {
  enemy: Enemy;
  player: Character;
  combat_active: boolean;
  player_turn: boolean;
  quiz_available: boolean;
  is_master_fight: boolean;
  log: string[];
}

export interface Rewards {
  gold: number;
  experience: number;
  level_up: boolean;
  level_up_gains: Record<string, number> | null;
  can_train: boolean;
}

export interface AttackResult {
  player_damage: number;
  player_hit: boolean;
  player_message: string;
  enemy_damage: number;
  enemy_hit: boolean;
  enemy_message: string;
  enemy_hp: number;
  player_hp: number;
  combat_over: boolean;
  victory: boolean;
  rewards: Rewards | null;
  log: string[];
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  difficulty: number;
  question_type: string;
}

export interface QuizResult {
  correct: boolean;
  damage: number;
  message: string;
  enemy_damage: number;
  enemy_hit: boolean;
  enemy_message: string;
  enemy_hp: number;
  player_hp: number;
  combat_over: boolean;
  victory: boolean;
  rewards: Rewards | null;
}

export interface HealResult {
  heal_amount: number;
  player_hp: number;
  player_max_hp: number;
  message: string;
  enemy_damage: number;
  enemy_hit: boolean;
  enemy_message: string;
  enemy_hp: number;
  combat_over: boolean;
  victory: boolean;
}

export function enterForest() {
  return post<CombatState>('/api/combat/enter-forest');
}

export function startMasterFight(level: number) {
  return post<CombatState>(`/api/combat/master-fight/${level}`);
}

export function combatAttack() {
  return post<AttackResult>('/api/combat/attack');
}

export function combatSkill() {
  return post<AttackResult>('/api/combat/skill');
}

export function combatHeal() {
  return post<HealResult>('/api/combat/heal');
}

export function combatRun() {
  return post<{ success: boolean; message: string }>('/api/combat/run');
}

export function quizStart() {
  return post<QuizQuestion>('/api/combat/quiz/start');
}

export function quizAnswer(selectedIndex: number) {
  return post<QuizResult>('/api/combat/quiz/answer', { selected_index: selectedIndex });
}

export function getCombatState() {
  return get<CombatState>('/api/combat/state');
}

// ---- Town ----

export interface BankInfo {
  gold: number;
  bank_gold: number;
  can_rob: boolean;
}

export interface BankTransaction {
  success: boolean;
  message: string;
  gold: number;
  bank_gold: number;
}

export interface RobberyResult {
  success: boolean;
  message: string;
  gold_change: number;
  gold: number;
  bank_gold: number;
}

export function getBank() {
  return get<BankInfo>('/api/town/bank');
}

export function bankDeposit(amount: number) {
  return post<BankTransaction>('/api/town/bank/deposit', { amount });
}

export function bankWithdraw(amount: number) {
  return post<BankTransaction>('/api/town/bank/withdraw', { amount });
}

export function bankRob() {
  return post<RobberyResult>('/api/town/bank/rob');
}

export interface HealerInfo {
  full_heal_cost: number;
  per_hp_cost: number;
  hp_missing: number;
  current_hp: number;
  max_hp: number;
  current_gold: number;
}

export interface HealerResult {
  success: boolean;
  message: string;
  hp_healed: number;
  gold_spent: number;
  current_hp: number;
  current_gold: number;
}

export function getHealer() {
  return get<HealerInfo>('/api/town/healer');
}

export function healerHeal(healType: string, amount?: number) {
  return post<HealerResult>('/api/town/healer/heal', { heal_type: healType, amount });
}

export interface ShopItem {
  index: number;
  name: string;
  price: number;
  stat_value: number;
  owned: boolean;
  can_buy: boolean;
}

export interface ShopList {
  items: ShopItem[];
  current_gold: number;
  current_item_index: number;
}

export interface BuyResult {
  success: boolean;
  message: string;
  gold_remaining: number;
  item_name: string;
}

export function listWeapons() {
  return get<ShopList>('/api/town/weapons');
}

export function buyWeapon(itemIndex: number) {
  return post<BuyResult>('/api/town/weapons/buy', { item_index: itemIndex });
}

export function listArmor() {
  return get<ShopList>('/api/town/armor');
}

export function buyArmor(itemIndex: number) {
  return post<BuyResult>('/api/town/armor/buy', { item_index: itemIndex });
}

export interface MasterInfo {
  level: number;
  name: string;
  greeting: string;
  can_challenge: boolean;
  exp_needed: number;
  current_exp: number;
}

export interface TrainingStatus {
  current_level: number;
  masters: MasterInfo[];
  can_challenge_current: boolean;
}

export function getTraining() {
  return get<TrainingStatus>('/api/town/training');
}

export interface Warrior {
  name: string;
  level: number;
  experience: number;
  class_type: string;
  weapon: string;
  armor: string;
  alive: boolean;
  total_kills: number;
  dragon_kills: number;
}

export function listWarriors() {
  return get<{ warriors: Warrior[] }>('/api/town/warriors');
}

export function getDailyNews() {
  return get<{ message: string }>('/api/town/daily-news');
}

// ---- Inn ----

export interface InnStatus {
  level: number;
  gold: number;
  gems: number;
  charm: number;
  inn_room: boolean;
  room_cost: number;
  bribe_cost: number;
  can_access_bar: boolean;
  married_to: string;
  flirted_violet: boolean;
}

export interface RoomRental {
  success: boolean;
  message: string;
  gold: number;
}

export interface GemTradeResult {
  success: boolean;
  message: string;
  gems: number;
  stat_changed: string;
  stat_value: number;
}

export interface VioletStatus {
  charm: number;
  married_to: string;
  violet_married: boolean;
  violet_husband: string | null;
  flirted_today: boolean;
  options: { charm_level: number; action: string; special: string | null }[];
}

export interface VioletResult {
  success: boolean;
  message: string;
  exp_gained: number;
  special: string | null;
  charm: number;
  married_to: string;
}

export interface BribeStatus {
  cost: number;
  gold: number;
  targets: { name: string; level: number; gold: number }[];
}

export interface BribeResult {
  success: boolean;
  message: string;
  exp_gained: number;
  gold_gained: number;
  gold: number;
}

export interface NameChangeResult {
  success: boolean;
  message: string;
  new_name: string;
}

export function getInnStatus() {
  return get<InnStatus>('/api/town/inn');
}

export function rentRoom() {
  return post<RoomRental>('/api/town/inn/rent-room');
}

export function gemTrade(stat: string) {
  return post<GemTradeResult>('/api/town/inn/gem-trade', { stat });
}

export function getVioletStatus() {
  return get<VioletStatus>('/api/town/inn/violet');
}

export function violetFlirt(charmLevel: number) {
  return post<VioletResult>('/api/town/inn/violet/flirt', { charm_level: charmLevel });
}

export function getBribeStatus() {
  return get<BribeStatus>('/api/town/inn/bribe');
}

export function bribeKill(targetName: string) {
  return post<BribeResult>('/api/town/inn/bribe', { target_name: targetName });
}

export function changeName(newName: string) {
  return post<NameChangeResult>('/api/town/inn/name-change', { new_name: newName });
}

// ---- Vault ----

export interface VaultStatus {
  connected: boolean;
  path: string | null;
  note_count: number;
  auto_detected: boolean;
}

export function getVaultStatus() {
  return get<VaultStatus>('/api/vault/status');
}

export function autoDetectVault() {
  return post<VaultStatus>('/api/vault/auto-detect');
}

export function setVaultPath(path: string) {
  return post<VaultStatus>('/api/vault/set-path', { path });
}

export interface Note {
  title: string;
  difficulty: number;
  tags: string[];
  age_days: number;
}

export function listNotes(limit = 50, offset = 0) {
  return get<{ notes: Note[]; total: number }>(`/api/vault/notes?limit=${limit}&offset=${offset}`);
}

// ---- Settings ----

export interface Settings {
  difficulty_mode: string;
  ai_narratives_enabled: boolean;
  quiz_attacks_enabled: boolean;
  ai_provider: string;
  claude_model: string;
  has_api_key: boolean;
  ollama_host: string;
  ollama_model: string;
}

export interface AIStatus {
  provider: string;
  available: boolean;
  status: string;
}

export function getSettings() {
  return get<Settings>('/api/settings');
}

export function updateSettings(updates: Partial<Settings & { claude_api_key: string }>) {
  return post<Settings>('/api/settings', updates);
}

export function getAIStatus() {
  return get<AIStatus>('/api/settings/ai');
}

// ---- IGM ----

export interface IGMResult {
  action: string;
  success: boolean;
  message: string;
  rewards?: Record<string, unknown>;
}

export interface CavernResult extends IGMResult {
  searches_remaining: number;
}

export function cavernExplore() {
  return post<CavernResult>('/api/igm/cavern/explore');
}

export function cavernSearch() {
  return post<CavernResult>('/api/igm/cavern/search');
}

export function getRiddle() {
  return get<{ riddle: string; answer_length: number }>('/api/igm/cavern/riddle');
}

export function answerRiddle(answer: string) {
  return post<CavernResult>('/api/igm/cavern/riddle', { answer });
}

export function fairyLearn() {
  return post<IGMResult>('/api/igm/fairy/learn');
}

export function fairyPractice() {
  return post<IGMResult>('/api/igm/fairy/practice');
}

export function fairyMeditate() {
  return post<IGMResult>('/api/igm/fairy/meditate');
}

export function fairyGather() {
  return post<IGMResult>('/api/igm/fairy/gather');
}

export function barakRead() {
  return post<{ action: string; message: string }>('/api/igm/barak/read');
}

export function barakStudy() {
  return post<{ action: string; message: string }>('/api/igm/barak/study');
}

export function barakTalk() {
  return post<{ action: string; message: string }>('/api/igm/barak/talk');
}

export interface XenonStatus {
  stored_gold: number;
  stored_gems: number;
  has_horse: boolean;
  horse_name: string;
  children: number;
  gold: number;
  gems: number;
}

export interface XenonResult {
  action: string;
  success: boolean;
  message: string;
  stored_gold: number;
  stored_gems: number;
  gold: number;
  gems: number;
}

export function getXenonStatus() {
  return get<XenonStatus>('/api/igm/xenon');
}

export function xenonTransaction(action: string, amount?: number, horseName?: string, tradeType?: string) {
  return post<XenonResult>('/api/igm/xenon/transaction', {
    action,
    amount,
    horse_name: horseName,
    trade_type: tradeType,
  });
}

export interface WerewolfStatus {
  is_werewolf: boolean;
  transformations: number;
  uses_today: number;
  gold: number;
}

export interface WerewolfResult {
  action: string;
  success: boolean;
  message: string;
  stat_changes?: Record<string, number>;
}

export function getWerewolfStatus() {
  return get<WerewolfStatus>('/api/igm/werewolf');
}

export function werewolfAccept() {
  return post<WerewolfResult>('/api/igm/werewolf/accept');
}

export function werewolfPractice() {
  return post<WerewolfResult>('/api/igm/werewolf/practice');
}

export function werewolfMeditate() {
  return post<WerewolfResult>('/api/igm/werewolf/meditate');
}

export function werewolfHowl() {
  return post<WerewolfResult>('/api/igm/werewolf/howl');
}

export interface GatewayResult {
  action: string;
  destination: string;
  message: string;
  rewards?: Record<string, unknown>;
  gems_remaining: number;
}

export function gatewayZycho() {
  return post<GatewayResult>('/api/igm/gateway/zycho');
}

export function gatewayDeath() {
  return post<GatewayResult>('/api/igm/gateway/death');
}

export function gatewayRandom() {
  return post<GatewayResult>('/api/igm/gateway/random');
}
